from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="AI Comic Generator")

app.include_router(router)


@app.get("/")
def home():
    return {"message": "AI Comic Generator API is running"}