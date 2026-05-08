import os
import pandas as pd
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# load the .env file so we don't leak the google api key on github
load_dotenv()

# shut up the annoying tokenizer warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def build_vector_db():
    print("loading inci dataset...")
    try:
        df = pd.read_csv("inci_ingredients_cleaned.csv")
    except:
        print("bro, where is the csv file?")
        return None

    # fill empty spaces just in case so it doesn't crash
    df = df.fillna("Not specified")

    docs = []
    for index, row in df.iterrows():
        # format the text for the ai to read easily
        text = f"Ingredient: {row['name']}\nScientific Name: {row['scientific_name']}\nWhat it does: {row['what_does_it_do']}\nGood for: {row['who_is_it_good_for']}\nAvoid if: {row['who_should_avoid']}"
        docs.append(text)

    print(f"processing {len(docs)} ingredients...")
    # chunking the text so it fits in memory
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100, length_function=len)
    chunks = splitter.create_documents(docs)

    print("loading embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")

    print("saving to chromadb...")
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory="./skincare_vector_db"
    )
    
    print("database is ready!")
    return db

# simple helper to join documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def ask_ciltkocum(db, user_query):
    print(f"\nuser asks: {user_query}")
    
    # get top 5 matches from the db
    retriever = db.as_retriever(search_kwargs={"k": 5})
    
    # using gemini 1.5 flash cause it's fast and cheap
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1) 
    
    # upgraded the prompt for better reasoning and strict regex matching for c#
    sys_prompt = """
    Sen "CiltKoçum" uygulamasının uzman dermatolojik asistanısın. Kullanıcıya şefkatli, net ve doğrudan çözüm odaklı yaklaşmalısın.

    GÖREVİN:
    1. Kullanıcının cilt problemini anla ve empati kur.
    2. Sağlanan veritabanı içeriğini kullanarak bu problemi çözecek EN İYİ 1 veya 2 etken maddeyi belirle.
    3. Neden bu maddeyi önerdiğini kısa ve anlaşılır bir dille açıkla.
    4. Eğer veritabanında bu madde için 'Kimler Uzak Durmalı' (Avoid if) uyarısı varsa, kullanıcıyı kesinlikle uyar.

    KIRMIZI ÇİZGİLER (ASLA YAPMA):
    - Asla "Veritabanına göre", "Bana verilen bilgilere göre" gibi yapay zeka olduğunu belli eden cümleler kurma.
    - Asla marka veya spesifik bir ürün adı önerme. Sadece etken madde/içerik öner.

    C# ENTEGRASYON KURALI (KRİTİK):
    Sistemimizin arka planda ürün eşleştirmesi yapabilmesi için, ön plana çıkardığın temel etken maddenin veritabanındaki İngilizce INCI adını MUTLAKA köşeli parantez içinde yaz. 
    Örnek format: "...tedavisi için [Salicylic Acid] harika bir tercih olacaktır." veya "...gözeneklerini temizlemek için [Niacinamide] kullanabilirsin."

    Veritabanı İçeriği:
    {context}

    Kullanıcı: {question}

    Uzman Yanıtı:
    """
    prompt = PromptTemplate.from_template(sys_prompt)
    
    # build the rag chain (lcel magic)
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print("ai is thinking...\n")
    response = chain.invoke(user_query)
    
    print("CiltKoçum AI:")
    print(response)
    return response

if __name__ == "__main__":
    db = build_vector_db()
    
    if db:
        # testing the pipeline
        test_q = "Burnumda çok fazla siyah nokta var ve cildim çok yağlı, ne yapmalıyım?"
        ask_ciltkocum(db, test_q)