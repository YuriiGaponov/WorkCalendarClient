from fastapi import APIRouter

from .interfaces import router as interface_router

router = APIRouter()
router.include_router(interface_router)

__all__ = ['router']
