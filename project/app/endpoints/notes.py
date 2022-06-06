from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.note import NoteCreate, NoteUpdate, Note, NoteGetWithTags, NoteGet
from app.database.models.tag import Tag
from app.database.repositories.notes_repository import NotesRepository
from app.database.repositories.tags_repository import TagsRepository
from app.responses import Message

router = APIRouter(
    prefix="/notes",
    tags=["Note"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[NoteGetWithTags], responses={'404': {'model': Message}})
async def get_notes(
        search: Optional[str] = None, tag: Optional[int] = None,
        sort_title: Optional[bool] = None, sort_date: Optional[bool] = None,
        session: AsyncSession = Depends(get_session)):
    notes_repository = NotesRepository(session)
    tags_repository = TagsRepository(session)

    db_tag: Optional[Tag] = None
    if tag is not None:
        db_tag: Optional[Tag] = await tags_repository.get_by_id(tag)
        if db_tag is None:
            return JSONResponse(status_code=404, content={'message': f"[ID:{tag}] Tag not found"})

    db_notes = await notes_repository.get_all(search, db_tag, sort_date, sort_title)
    return db_notes


@router.get("/{note_id}", response_model=NoteGetWithTags, responses={'404': {'model': Message}})
async def get_note(note_id: int, session: AsyncSession = Depends(get_session)):
    notes_repository = NotesRepository(session)
    db_note = await notes_repository.get_by_id(note_id)
    if db_note is None:
        return JSONResponse(status_code=404, content={'message': f"[ID:{note_id}] Note not found"})

    return db_note


@router.post("/", response_model=NoteGet, responses={'404': {'model': Message}})
async def add_note(note_create: NoteCreate, session: AsyncSession = Depends(get_session)):
    notes_repository = NotesRepository(session)
    tags_repository = TagsRepository(session)

    db_tags: list[Tag] = []
    for tag_id in note_create.tags_ids:
        db_tag: Optional[Tag] = await tags_repository.get_by_id(tag_id)
        if db_tag is None:
            return JSONResponse(status_code=404, content={'message': f"[ID:{tag_id}] Tag not found"})

        db_tags.append(db_tag)

    db_note = notes_repository.create(note_create, db_tags)

    await notes_repository.commit()
    await notes_repository.refresh(db_note)

    return db_note


@router.put("/{note_id}", response_model=NoteGet, responses={'404': {'model': Message}})
async def update_note(note_id: int, note_update: NoteUpdate, session: AsyncSession = Depends(get_session)):
    notes_repository = NotesRepository(session)
    tags_repository = TagsRepository(session)

    db_note: Optional[Note] = await notes_repository.get_by_id(note_id)
    if db_note is None:
        return JSONResponse(status_code=404, content={'message': f"[ID:{note_id}] Note not found"})

    db_tags: Optional[list[Tag]] = None
    if note_update.tags_ids is not None and len(note_update.tags_ids) != 0:
        db_tags = []
        for tag_id in note_update.tags_ids:
            db_tag: Optional[Tag] = await tags_repository.get_by_id(tag_id)
            if db_tag is None:
                return JSONResponse(status_code=404, content={'message': f"[ID:{tag_id}] Tag not found"})

            db_tags.append(db_tag)

    db_note = notes_repository.update(db_note, note_update, db_tags)

    await notes_repository.commit()
    await notes_repository.refresh(db_note)

    return db_note


@router.delete("/{note_id}", responses={'404': {'model': Message}, '200': {'model': Message}})
async def delete_note(note_id: int, session: AsyncSession = Depends(get_session)):
    notes_repository = NotesRepository(session)

    db_note: Optional[Note] = await notes_repository.get_by_id(note_id)
    if db_note is None:
        return JSONResponse(status_code=404, content={'message': f"[ID:{note_id}] Note not found"})

    await notes_repository.delete(db_note)
    await notes_repository.commit()

    return JSONResponse(status_code=200, content={'message': f'[ID:{note_id}] Note deleted successfully'})
