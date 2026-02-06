from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import AsyncMongoClient

from app.core.config import config
from app.models import Student
from app.routers import students


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    # Startup
    mongo_client = AsyncMongoClient(str(config.mongodb_uri))
    await init_beanie(database=mongo_client.db_name, document_models=[Student])

    yield

    # Shutdown
    await mongo_client.close()


app = FastAPI(title="Student Course API", lifespan=lifespan)


# Set all CORS enabled origins
if config.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(students.router)
