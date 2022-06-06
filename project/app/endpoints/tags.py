from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.tag import TagCreate, TagUpdate, Tag, TagGetWithNotes, TagGet
from app.database.repositories.notes_repository import NotesRepository
from app.database.repositories.tags_repository import TagsRepository
from app.responses import Message

router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[TagGetWithNotes])
async def get_tags(session: AsyncSession = Depends(get_session)):
    tags_repository = TagsRepository(session)

    db_tags = await tags_repository.get_all()

    return db_tags


@router.get("/{tag_id}", response_model=TagGetWithNotes, responses={'404': {'model': Message}})
async def get_tag(tag_id: int, session: AsyncSession = Depends(get_session)):
    tags_repository = TagsRepository(session)

    db_tag: Optional[Tag] = await tags_repository.get_by_id(tag_id)
    if db_tag is None:
        return JSONResponse(status_code=404, content={'message': f"[ID:{db_tag}] Tag not found"})

    return db_tag


@router.post("/", response_model=TagGet)
async def add_tag(tag_create: TagCreate, session: AsyncSession = Depends(get_session)):
    tags_repository = TagsRepository(session)

    db_tag = tags_repository.create(tag_create)

    await tags_repository.commit()
    await tags_repository.refresh(db_tag)

    return db_tag


@router.put("/{tag_id}", response_model=TagGet, responses={'404': {'model': Message}})
async def update_tag(tag_id: int, tag_update: TagUpdate, session: AsyncSession = Depends(get_session)):
    tags_repository = TagsRepository(session)

    db_tag: Optional[Tag] = await tags_repository.get_by_id(tag_id)
    if db_tag is None:
        return JSONResponse(status_code=404, content={'message': f"[ID:{db_tag}] Tag not found"})

    db_tag = tags_repository.update(db_tag, tag_update)

    await tags_repository.commit()
    await tags_repository.refresh(db_tag)

    return db_tag


@router.delete("/{tag_id}", responses={'404': {'model': Message}, '200': {'model': Message}})
async def delete_tag(tag_id: int, session: AsyncSession = Depends(get_session)):
    tags_repository = TagsRepository(session)

    db_tag: Optional[Tag] = await tags_repository.get_by_id(tag_id)
    if db_tag is None:
        return JSONResponse(status_code=404, content={'message': f"[ID:{db_tag}] Tag not found"})

    if db_tag.notes is not None:
        db_tag.notes.clear()

    await tags_repository.delete(db_tag)
    await tags_repository.commit()

    return JSONResponse(status_code=200, content={'message': f'[ID:{tag_id}] Tag deleted successfully'})
