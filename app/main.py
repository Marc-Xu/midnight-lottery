"""
FastAPI application instantiation and route definitions, leveraging service layer.
"""

import logging

from fastapi import FastAPI, HTTPException, Request
from sqlalchemy.exc import IntegrityError, DataError

from app.config import Settings
from app.data_access_layer.database import engine, Base
from app.api.v1.participant_endpoints import router as participant_router
from app.exceptions import NotFoundError, ValidationError

# Initialize settings and logging
settings = Settings()
logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)
logger = logging.getLogger(__name__)

# Create all database tables
Base.metadata.create_all(bind=engine)

# Instantiate FastAPI
app = FastAPI(
    title="Midnight Lottery",
    debug=settings.debug,
)


# Register exception handlers
@app.exception_handler(NotFoundError)
async def not_found_handler(_: Request, exc: NotFoundError):
    """
    Handle cases where a resource is not found.
    """
    raise HTTPException(status_code=404, detail=str(exc))


@app.exception_handler(ValidationError)
async def validation_exception_handler(_: Request, exc: ValidationError):
    """
    Handle request validation errors raised in service layer.
    """
    raise HTTPException(status_code=422, detail=str(exc))


@app.exception_handler(ValueError)
async def value_error_handler(_: Request, exc: ValueError):
    """
    Handle ValueError raised in service layer.
    """
    raise HTTPException(status_code=400, detail=str(exc))


@app.exception_handler(IntegrityError)
async def integrity_error_handler(_: Request, exc: IntegrityError):
    """
    Handle IntegrityError from database operations.
    """
    raise HTTPException(status_code=400, detail=str(exc.orig.args))


@app.exception_handler(DataError)
async def data_error_handler(_: Request, exc: DataError):
    """
    Handle DataError (e.g., invalid types or out of range values).
    """
    raise HTTPException(status_code=422, detail=str(exc))


@app.get("/health", summary="Health check endpoint")
def health() -> dict:
    """
    Health endpoint to verify service is running.
    """
    return {"status": "ok"}


app.include_router(participant_router, prefix="/participants", tags=["Participants"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.debug)
