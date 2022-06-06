from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship

from app.database.models.links.tagnote import TagNote


class NoteBase(SQLModel):
    __tablename__ = "notes"

    title: str = Field(max_length=256, nullable=False, default="NoTitle")
    text: str = Field(max_length=2048, nullable=False, default="NoText")


class Note(NoteBase, table=True):
    id: int = Field(default=None, primary_key=True)
    tags: List["Tag"] = Relationship(back_populates="notes", link_model=TagNote)
    created_at: datetime = Field(nullable=False, default=datetime.utcnow())


class NoteGet(NoteBase):
    id: int
    created_at: datetime


class NoteGetWithTags(NoteGet):
    tags: list["TagGet"] = []


class NoteCreate(NoteBase):
    tags_ids: list[int]


class NoteUpdate(SQLModel):
    title: Optional[str] = None
    text: Optional[str] = None
    tags_ids: Optional[list[int]] = None


from app.database.models.tag import TagGet, Tag

NoteGetWithTags.update_forward_refs()
