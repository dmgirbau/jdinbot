# src/jdinbot/api/v1/routers.py
from fastapi import APIRouter
from .endpoints import health

router = APIRouter(prefix="/v1")

router.include_router(health.router)