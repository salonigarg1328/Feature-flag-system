from fastapi import FastAPI

from app.routers import auth

app = FastAPI(title="Feature Flag System")

app.include_router(auth.router)


@app.get("/")
def home():
    return {"message": "Backend is running"}