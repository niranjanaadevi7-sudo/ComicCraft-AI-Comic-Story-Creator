from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router


app = FastAPI(title="AI Comic Generator")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "AI Comic Generator API is running"
    }
