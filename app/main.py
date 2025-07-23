"""
FastAPI application instantiation and route definitions, leveraging service layer.
"""

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, HTTPException, Request
from sqlalchemy.exc import IntegrityError, DataError

from app.api.v1.draw_endpoints import daily_draw, create_draw
from app.config import Settings
from app.data_access_layer.database import engine, Base
from app.api.v1.participant_endpoints import router as participant_router
from app.api.v1.draw_endpoints import router as draw_router
from app.api.v1.ballot_endpoints import router as ballot_router
from app.exceptions import NotFoundError, ValidationError

# Initialize settings and logging
settings = Settings()
logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)
logger = logging.getLogger(__name__)

# Create all database tables
Base.metadata.create_all(bind=engine)


# Schedule a draw
def run_daily_draw():
    daily_draw()  # draw a winner
    create_draw()  # open a new lottery


scheduler = BackgroundScheduler(timezone="Europe/Amsterdam")
scheduler.add_job(run_daily_draw, "cron", hour=0, minute=0)
scheduler.start()


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
app.include_router(draw_router, prefix="/draws", tags=["Draws"])
app.include_router(ballot_router, prefix="/ballots", tags=["Ballots"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.debug)
