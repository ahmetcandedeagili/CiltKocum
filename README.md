# ✨ CiltKoçum - AI Skincare Laboratory

![Project Status](https://img.shields.io/badge/Status-Production_Ready-success)
![Architecture](https://img.shields.io/badge/Architecture-Microservices-blue)
![C#](https://img.shields.io/badge/Backend-C%23_ASP.NET_Core-512BD4)
![Python](https://img.shields.io/badge/AI_Microservice-Python_FastAPI-3776AB)

CiltKoçum is an AI-powered hybrid e-commerce assistant built on a microservices architecture. It analyzes user skin concerns through Natural Language Processing (NLP) and recommends personalized active ingredients and clinical products from global cosmetic datasets (Sephora & INCI).

## 🏗️ System Architecture

The project utilizes a dual-language microservices architecture to leverage the best of both ecosystems:

### 1. Web Presentation & Data Layer (C# / ASP.NET Core)
* **Framework:** ASP.NET Core 8.0 MVC
* **Database:** MS SQL Server with Entity Framework Core (Code-First)
* **Authentication:** Secure Cookie-based Authentication
* **Communication:** Asynchronous REST API calls via Data Transfer Object (DTO) pattern.
* **UI/UX:** Sephora-inspired minimalist design, Bootstrap 5, fully responsive.

### 2. AI & NLP Microservice (Python / FastAPI)
* **RAG Pipeline:** Retrieval-Augmented Generation using **LangChain**.
* **Vector Database:** **ChromaDB** integrated with HuggingFace embedding models for semantic search of cosmetic ingredients.
* **LLM Engine:** Google Gemini 2.5 Flash for reasoning and JSON generation.
* **Data Processing:** Kaggle Sephora datasets processed via **Pandas**.

## 🚀 Key Features
- **Molecular Diagnostics:** Users can type their skin issues in natural language, and the AI determines the root cause.
- **Product Matching:** AI-driven matching of the targeted active ingredient with real-world Sephora products.
- **Analysis History:** Authenticated users have a personalized dashboard to track their past clinical assessments.
- **Secure Architecture:** Complete isolation of the AI engine from the user-facing web application.

## ⚙️ Installation & Setup

### Prerequisites
- .NET 8.0 SDK
- Python 3.10+
- SQL Server

### AI Microservice Setup
1. Navigate to the AI service directory: `cd AI-Service`
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `.\venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file in this directory and add your API Key: `GOOGLE_API_KEY=your_key_here`
6. Run the server: `python api.py` (Runs on port 8000)

### Web App Setup
1. Open `Web-App/CiltKocum.Web.sln` in Visual Studio.
2. Open Package Manager Console and run: `Update-Database` to create SQL tables.
3. Set the project as Startup Project and Run.

## 👨‍💻 Developer
Developed by **Ahmet Can Dedeağılı**.
Passionate about blending Artificial Intelligence technologies with modern software architectures.

[LinkedIn Profile](https://linkedin.com/in/ahmet-can-dedeağili-3a9985236) | [GitHub Profile](https://github.com/ahmetcandedeagili)


Turkish Version (Türkçe Versiyon)

# ✨ CiltKoçum - Yapay Zeka Destekli Cilt Bakım Laboratuvarı

![Project Status](https://img.shields.io/badge/Durum-Canlıya_Hazır-success)
![Architecture](https://img.shields.io/badge/Mimari-Mikroservis-blue)
![C#](https://img.shields.io/badge/Backend-C%23_ASP.NET_Core-512BD4)
![Python](https://img.shields.io/badge/AI_Microservice-Python_FastAPI-3776AB)

CiltKoçum, mikroservis mimarisi üzerine inşa edilmiş yapay zeka destekli hibrit bir e-ticaret asistanıdır. Kullanıcıların cilt sorunlarını Doğal Dil İşleme (NLP) ile analiz eder ve küresel kozmetik veri setlerinden (Sephora & INCI) kişiselleştirilmiş etken maddeler ve klinik ürünler önerir.

## 🏗️ Sistem Mimarisi

Proje, her iki ekosistemin de en iyi özelliklerinden faydalanmak için çift dilli bir mikroservis mimarisi kullanır:

### 1. Web Sunum ve Veri Katmanı (C# / ASP.NET Core)
* **Framework:** ASP.NET Core 8.0 MVC
* **Veritabanı:** Entity Framework Core (Code-First) ile MS SQL Server
* **Kimlik Doğrulama:** Güvenli Cookie (Çerez) tabanlı yetkilendirme.
* **İletişim:** DTO (Data Transfer Object) deseni ile asenkron REST API çağrıları.
* **UI/UX:** Sephora ilhamlı minimalist tasarım, Bootstrap 5, tam mobil uyumlu (responsive).

### 2. Yapay Zeka & NLP Mikroservisi (Python / FastAPI)
* **RAG Boru Hattı:** **LangChain** kullanılarak Retrieval-Augmented Generation (Genişletilmiş Geri Getirme Üretimi).
* **Vektör Veritabanı:** Kozmetik bileşenlerin anlamsal araması için HuggingFace embedding modelleriyle entegre **ChromaDB**.
* **LLM Motoru:** Akıl yürütme ve yapılandırılmış JSON üretimi için Google Gemini 2.5 Flash.
* **Veri İşleme:** **Pandas** ile işlenen Kaggle Sephora veri setleri.

## 🚀 Temel Özellikler
- **Moleküler Teşhis:** Kullanıcılar cilt sorunlarını doğal dille yazabilir ve yapay zeka problemin temel nedenini belirler.
- **Ürün Eşleştirme:** Hedeflenen etken maddenin gerçek dünya Sephora ürünleriyle yapay zeka destekli eşleştirilmesi.
- **Analiz Geçmişi:** Giriş yapan kullanıcılar, geçmiş klinik değerlendirmelerini takip edebilecekleri kişiselleştirilmiş bir panele sahiptir.
- **Güvenli Mimari:** Yapay zeka motorunun, kullanıcıya dönük web uygulamasından tamamen izole edilmesi.

## ⚙️ Kurulum ve Çalıştırma

### Gereksinimler
- .NET 8.0 SDK
- Python 3.10+
- SQL Server

### Yapay Zeka Mikroservisi Kurulumu
1. AI servisi dizinine gidin: `cd AI-Service`
2. Sanal ortam oluşturun: `python -m venv venv`
3. Ortamı aktif edin: `.\venv\Scripts\activate` (Windows)
4. Gereksinimleri yükleyin: `pip install -r requirements.txt`
5. Bu dizinde bir `.env` dosyası oluşturun ve API Anahtarınızı ekleyin: `GOOGLE_API_KEY=api_anahtariniz_buraya`
6. Sunucuyu başlatın: `python api.py` (8000 portunda çalışır)

### Web Uygulaması Kurulumu
1. Visual Studio'da `Web-App/CiltKocum.Web.sln` dosyasını açın.
2. Package Manager Console'u açın ve SQL tablolarını oluşturmak için şu komutu çalıştırın: `Update-Database`
3. Projeyi Başlangıç Projesi (Startup Project) olarak ayarlayın ve çalıştırın.

## 👨‍💻 Geliştirici
**Ahmet Can Dedeağılı** tarafından geliştirilmiştir.
Yapay zeka teknolojilerini modern yazılım mimarileriyle harmanlama konusunda tutkulu bir Bilgisayar Mühendisliği öğrencisi.

[LinkedIn Profili](https://linkedin.com/in/ahmet-can-dedeağili-3a9985236) | [GitHub Profili](https://github.com/ahmetcandedeagili)
