from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.models.tag import Tag, TagCreate, TagUpdate


class TagsRepository(object):
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_all(self) -> list[Tag]:
        query = select(Tag).options(selectinload(Tag.notes))
        execute = await self.session.execute(query)

        db_tags: list[Tag] = execute.scalars().all()
        return db_tags

    async def get_by_id(self, tag_id: int) -> Optional[Tag]:
        query = select(Tag).where(Tag.id == tag_id).options(selectinload(Tag.notes))
        execute = await self.session.execute(query)

        db_tag: Optional[Tag] = execute.scalar_one_or_none()
        return db_tag

    def create(self, tag_create: TagCreate) -> Tag:
        db_tag = Tag.from_orm(tag_create)

        self.session.add(db_tag)

        return db_tag

    def update(self, db_tag: Tag, tag_update: TagUpdate) -> Optional[Tag]:
        for var, value in vars(tag_update).items():
            if vars(db_tag).get(var) is None:
                continue
            setattr(db_tag, var, value) if value else None

        self.session.add(db_tag)
        return db_tag

    async def delete(self, db_tag: Tag) -> None:
        if db_tag.notes is not None:
            db_tag.notes.clear()

        await self.session.delete(db_tag)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, db_tag: Tag):
        await self.session.refresh(db_tag)
