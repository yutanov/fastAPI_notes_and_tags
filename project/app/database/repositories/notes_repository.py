from typing import Optional

from sqlalchemy import desc, asc
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.models.note import Note, NoteCreate, NoteUpdate
from app.database.models.tag import Tag


class NotesRepository(object):
    def __init__(self, session):
        self.session = session

    async def get_all(
            self,
            search_title: Optional[str] = None, db_tag: Optional[Tag] = None,
            sort_date: Optional[bool] = None, sort_title: Optional[bool] = None) -> list[Note]:
        query = select(Note).options(selectinload(Note.tags))

        if search_title is not None:
            if '*' in search_title or '_' in search_title:
                looking_for = search_title.replace('_', '__') \
                    .replace('*', '%') \
                    .replace('?', '_')
            else:
                looking_for = f'%{search_title}%'

            query = query.where(Note.title.ilike(looking_for.lower()))

        if db_tag is not None:
            query = query.where(Note.tags.contains(db_tag))

        if sort_title is not None:
            if sort_title is True:
                query = query.order_by(desc(Note.title))

            elif sort_title is False:
                query = query.order_by(asc(Note.title))

        if sort_date is not None:
            if sort_date is True:
                query = query.order_by(desc(Note.created_at))

            elif sort_date is False:
                query = query.order_by(asc(Note.created_at))

        execute = await self.session.execute(query)

        db_notes: list[Note] = execute.scalars().all()
        return db_notes

    async def get_by_id(self, note_id: int) -> Optional[Note]:
        query = select(Note).where(Note.id == note_id).options(selectinload(Note.tags))
        execute = await self.session.execute(query)

        db_note: Optional[Note] = execute.scalar_one_or_none()
        return db_note

    def create(self, note_create: NoteCreate, tags: list[Tag]) -> Note:
        db_note = Note.from_orm(note_create)
        db_note.tags = tags

        self.session.add(db_note)

        return db_note

    def update(self, db_note: Note, note_update: NoteUpdate, tags: Optional[list[Tag]] = None) -> Optional[Note]:
        if tags is not None:
            db_note.tags.clear()
            if len(tags) != 0:
                db_note.tags = tags

        for var, value in vars(note_update).items():
            if vars(db_note).get(var) is None:
                continue
            setattr(db_note, var, value) if value else None

        self.session.add(db_note)
        return db_note

    async def delete(self, db_note: Note) -> None:
        if db_note.tags is not None:
            db_note.tags.clear()

        await self.session.delete(db_note)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, db_note: Note):
        await self.session.refresh(db_note)
