from fastapi import APIRouter
from app.endpoints import notes, tags

router = APIRouter()
router.include_router(notes.router)
router.include_router(tags.router)
