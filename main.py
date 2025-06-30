from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import cohere
import asyncio
import os

# --------- Singleton Classes ---------
class EmbeddingSingleton:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer("BAAI/bge-small-en-v1.5")
        return cls._model

class FAISSSingleton:
    _index = None
    _texts = None

    @classmethod
    def get_index_and_texts(cls):
        if cls._index is None:
            df = pd.read_csv("data/plant_diseases_treatment.csv")

            def combine_columns(row):
                return f"النبات: {row['اسم النبات']}, المرض: {row['اسم المرض']}, العلاج: {row['العلاج']}, طريقة الرش: {row['طريقة الرش']}, توقيت الرش: {row['توقيت الرش']}, إجراءات إضافية: {row['إجراءات إضافية']}"

            texts = df.apply(combine_columns, axis=1).tolist()
            embedding_model = EmbeddingSingleton.get_model()
            embeddings = embedding_model.encode(texts, show_progress_bar=True)

            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings)

            cls._index = index
            cls._texts = texts

        return cls._index, cls._texts

class CohereSingleton:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            api_key = os.getenv("API_KEY")
            cls._client = cohere.Client(api_key)
        return cls._client

# --------- FastAPI App ---------
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Chatbot API is running"}

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question", "")

    # Get Singleton instances
    embedding_model = EmbeddingSingleton.get_model()
    index, texts = FAISSSingleton.get_index_and_texts()
    co = CohereSingleton.get_client()

    # Search
    query_vector = embedding_model.encode([question])
    D, I = index.search(query_vector, k=3)
  
    retrieved_context = "\n".join([texts[i] for i in I[0]])

    prompt = f"""
السؤال: {question}
المعلومات: {retrieved_context}
أجب بدقة بجملة واحدة فقط دون إضافة أي معلومات خارجية.
"""

    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=100,
        temperature=0.3
    )

    return {"answer": response.generations[0].text}
