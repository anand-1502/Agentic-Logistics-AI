# app/main.py

from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Agentic AI Logistics Risk Backend",
    description="Backend APIs for uploading, scoring risks, and monitoring shipments",
    version="1.0.0",
)

# Include API routes
app.include_router(router)

# Root welcome endpoint
@app.get("/")
def read_root():
    return {"message": "🚛 Welcome to Agentic AI Logistics Risk API"}
