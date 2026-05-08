import os
import uvicorn
import re
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# --- LANGCHAIN & AI LIBRARIES ---
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

# Load secrets from the .env file into the system environment
load_dotenv()

# Securely fetch the API key without exposing it in the codebase
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("⚠️ GOOGLE_API_KEY is missing! Please check your .env file.")

# initialize the fastapi app
app = FastAPI(
    title="CiltKocum AI Brain",
    description="AI Powered Skincare Assistant (Local DB Version)",
    version="3.1.0" 
)

# --- DATA MODELS (JSON SCHEMAS) ---
class UserRequest(BaseModel):
    query: str

# renamed from ScrapedProduct to RecommendedProduct since we are not scraping anymore
class RecommendedProduct(BaseModel):
    name: str
    price: str
    image_url: str
    purchase_link: str

class AiResponse(BaseModel):
    response_text: str
    active_ingredient: str
    # keeping the json key as "live_products" so we don't break the C# DTO
    live_products: List[RecommendedProduct] 

# global rag chain variable
qa_chain = None

# simple helper to join document texts
def combine_documents(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# --- LOCAL DATABASE PRODUCT MATCHER ---
def find_products_in_db(active_ingredient: str) -> List[RecommendedProduct]:
    products = []
    print(f"🔍 SEARCHING LOCAL DB: Looking for Sephora products containing '{active_ingredient}'...")
    
    try:
        # load the sephora products database
        df = pd.read_csv("sephora_skincare_products.csv")
        
        # fill empty ingredient rows to prevent pandas errors
        df['ingredients'] = df['ingredients'].fillna('')
        
        # find products where the ingredients column contains our active ingredient (case insensitive)
        matched_df = df[df['ingredients'].str.contains(active_ingredient, case=False, na=False)].head(3)
        
        for _, row in matched_df.iterrows():
            products.append(RecommendedProduct(
                name=f"{row['brand_name']} - {row['product_name']}",
                price=f"${row['price_usd']}",
                image_url="https://via.placeholder.com/150", # sephora dataset lacks images, using placeholder
                purchase_link="https://www.sephora.com" # default link
            ))
            
        if not products:
            print("⚠️ No exact match found in DB, generating a generic fallback product.")
            
    except Exception as e:
        print(f"⚠️ Database search error: {e}")
        
    # fallback test data if the dataset is missing or no matches found
    if not products:
        products.append(RecommendedProduct(
            name=f"Generic - {active_ingredient} Serum",
            price="$25.00",
            image_url="https://via.placeholder.com/150",
            purchase_link="https://example.com"
        ))
        
    return products

# --- SYSTEM STARTUP (LOADING AI & DB) ---
@app.on_event("startup")
def startup_event():
    global qa_chain
    print("🚀 MICROSERVICE STARTING: Loading DB and AI models...")
    try:
        # load the cleaned inci dataset
        loader = CSVLoader(file_path="inci_ingredients_cleaned.csv", encoding="utf-8")
        docs = loader.load()
        
        # setup embeddings and vector database
        embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
        vector_db = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory="./skincare_vector_db")
        retriever = vector_db.as_retriever(search_kwargs={"k": 4})
        
        # initialize the LLM (Gemini 2.5 Flash)
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

        # hybrid prompt instruction for the AI
        system_prompt = """
        Sen "CiltKoçum" platformunun Yapay Zeka Cilt Bakım Asistanısın. 
        Kullanıcının sorununu analiz et ve ona kullanması gereken etken maddeyi bul.

        KURALLAR:
        Cevabının EN BAŞINA, tespit ettiğin etken maddeyi mutlaka köşeli parantez içinde yaz. 
        Örnek format:
        [Salicylic Acid]
        Cildindeki yağlanma ve siyah noktalar için Salisilik Asit kullanmalısın...

        Veritabanı İçeriği:
        {context}

        Kullanıcı Sorusu: {input}
        """
        prompt = PromptTemplate.from_template(system_prompt)
        
        # build the LCEL chain
        qa_chain = (
            {"context": retriever | combine_documents, "input": RunnablePassthrough()} 
            | prompt 
            | llm 
            | StrOutputParser()
        )
        print("✅ CiltKocum AI is ready to accept requests!")
    except Exception as e:
        print(f"❌ Critical startup error: {e}")

# --- API ENDPOINT (COMMUNICATION WITH C#) ---
@app.post("/yapay-zeka/sor", response_model=AiResponse)
async def ask_ai(request: UserRequest):
    if qa_chain is None:
        raise HTTPException(status_code=500, detail="AI engine is not loaded yet.")
    
    try:
        # 1. get the raw text response from the LLM
        raw_response = qa_chain.invoke(request.query)
        
        # 2. extract the active ingredient using regex (e.g., [Salicylic Acid])
        match = re.search(r'\[(.*?)\]', raw_response)
        
        if match:
            active_ingredient = match.group(1).strip()
            # clean the bracketed text from the main response
            clean_response = raw_response.replace(f"[{active_ingredient}]", "").strip()
            clean_response = clean_response.lstrip('\n').strip()
        else:
            active_ingredient = "Cilt Bakım"
            clean_response = raw_response

        # 3. find matching products from our local Sephora CSV
        recommended_products = find_products_in_db(active_ingredient)
        
        # 4. return the packaged JSON data to C#
        return AiResponse(
            response_text=clean_response,
            active_ingredient=active_ingredient,
            live_products=recommended_products
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # run the server on localhost
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)