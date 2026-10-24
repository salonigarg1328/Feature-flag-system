from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth
from app.routers import auth, flags
from app.routers import auth, environments, flags

app = FastAPI(title="Feature Flag System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(flags.router)
app.include_router(environments.router)

@app.get("/")
def home():
    return {"message": "Backend is running"}