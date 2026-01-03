from fastapi import FastAPI
from app.api.exception_handler import app_exception_handler, validation_exception_handler
from app.exceptions.base import AppException
from app.api.controller import movie_controller 
from app.db.session import SessionLocal
from fastapi.exceptions import RequestValidationError
from app.logging_config import setup_logging

logger = setup_logging()

app = FastAPI(
    title="Movie Rating System",
    description="Web API format",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.include_router(movie_controller.router)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete")
