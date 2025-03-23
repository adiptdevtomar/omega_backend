from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.v1.endpoints.nlp import router as example_router
from app.api.v1.endpoints.auth import router as auth_router
from app.utils.error_handlers import (
    http_exception_handler,
    general_exception_handler,
    custom_exception_handler,
    CustomException,
)
from app.utils.response_formatter import format_response
from app.utils.mongodb import get_collection
import logging
from transformers import pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to logging.DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Define lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Server is starting...")
    collection = get_collection("user_otps")
    collection.create_index("expires_at", expireAfterSeconds=0)

    # Load the advanced emotion detection pipeline
    # logger.info("Loading advanced emotion detection pipeline...")
    # app.state.emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
    # logger.info("Advanced emotion detection pipeline loaded successfully.")

    # Load the question-answering pipeline
    # logger.info("Loading question-answering pipeline...")
    # app.state.qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
    # logger.info("Question-answering pipeline loaded successfully.")

    yield  # Application runs during this time

    # Shutdown logic
    logger.info("Server is shutting down...")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Omega Backend API",
    description="API documentation for Omega Backend",
    version="1.0.0",
    docs_url="/docs",  # Ensure this is not set to None
    redoc_url="/redoc",  # Optional: Enable ReDoc documentation
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(CustomException, custom_exception_handler)

# Global response formatting middleware
@app.middleware("http")
async def format_response_middleware(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 200 and response.media_type == "application/json":
        original_body = await response.body()
        formatted_body = format_response(data=original_body)
        return JSONResponse(content=formatted_body, status_code=response.status_code)
    return response

# Include routers
app.include_router(example_router, prefix="/api/v1/examples", tags=["examples"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"info": "Welcome to the Omega Backend API!"}