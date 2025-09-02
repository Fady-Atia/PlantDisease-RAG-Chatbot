## Planet Diseases -Rag- Arabic Chatbot project 
The aim of this project is to make it easier for anyone to use our application to learn more about plant diseases and how to treat them

## Requirements
- python 3.8 

 ### Install python using Anaconda 
 1) Download and install Anaconda from [here]( https://www.anaconda.com/download )

 2) Create a new environment  using the following command : 

      ```
      conda create -p myenv python==3.8 
      ```
3) Activate the environment :

      ```
       conda activate ./myenv 
     ```
## ⚙️ Tech Stack  
- **Python 3.8+**  
- **FastAPI** (for API endpoints)  
- **Sentence Transformers** (`BAAI/bge-small-en-v1.5`) for embeddings  
- **FAISS** for similarity search  
- **Cohere API** for answer generation  
- **Pandas** for dataset handling  
- **dotenv** for environment variables  

---

## 📂 Project Structure  
```
├── main.py                       # FastAPI application
├── data/
│   └── plant_diseases_treatment.csv   # Dataset (plants, diseases, treatments)
├── .env                          # API keys and environment variables
├── requirements.txt              # Dependencies
└── README.md                     # Project documentation
```


---

## 🔑 Environment Variables  
Create a `.env` file in the project root and add your **Cohere API key**:  

```env
API_KEY=your_cohere_api_key_here
```

📊 Dataset Format

The dataset should be a CSV file with the following columns:

اسم النبات (Plant Name)

اسم المرض (Disease Name)

العلاج (Treatment)

طريقة الرش (Spray Method)

توقيت الرش (Spray Timing)

إجراءات إضافية (Additional Actions)

📡 API Endpoints
✅ Root Endpoint

## GET /

{
  "message": "Chatbot API is running"
}

🌿 Ask Question

## POST /ask

Request
{
  "question": "ما هو علاج مرض الصدأ في القمح؟"
}

Response
{
  "answer": "النبات: القمح، المرض: الصدأ، العلاج: مبيد فطري مناسب..."
}


# 🧪 Example Workflow

User asks:

"ما هو علاج اللفحة المتأخرة في البطاطس؟"

The API retrieves related rows from the dataset.

Cohere generates a concise one-sentence answer
