from fastapi import FastAPI

from app.api import router as api_router

app = FastAPI(title="Student Course API")

app.include_router(api_router)
