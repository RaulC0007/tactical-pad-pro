from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]
    PROJECT_NAME: str = "Tactical Pad API"

    class Config:
        env_file = ".env"


settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para gestión táctica de fútbol",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "🚀 Tactical Pad API está corriendo", "status": "online"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "db": "pending_connection"}