# app/main.py
from fastapi import FastAPI
from .routes import router

app = FastAPI()
app.include_router(router)

# Run server
# Command: uvicorn app.main:app --reload
