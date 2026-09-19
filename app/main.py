"""FeatureFlow — intentional brownfield training starter."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .api import router as api_router
from .database import init_db
from .web import router as web_router

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="FeatureFlow",
    description="Brownfield training starter — intentionally imperfect.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router)
app.include_router(web_router)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
