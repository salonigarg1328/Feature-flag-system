from fastapi import FastAPI

app = FastAPI(title="Feature Flag System")

@app.get("/")
def home():
    return {"message": "Backend is running"}