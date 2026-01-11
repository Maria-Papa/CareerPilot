from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine, Base
from app.api.v1 import router

Base.metadata.create_all(bind=engine)

# Create all database tables (for SQLite dev mode)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CareerPilot API",
    version="1.0.0",
    description="Backend API for the CareerPilot application",
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Career Pilot backend running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
