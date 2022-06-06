from datetime import datetime
from typing import List

from sqlmodel import SQLModel, Field, Relationship

from app.database.models.links.tagnote import TagNote


class TagBase(SQLModel):
    __tablename__ = "tags"

    name: str = Field(max_length=256, nullable=False, default="NoName")


class Tag(TagBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(nullable=False, default=datetime.utcnow())
    notes: List["Note"] = Relationship(back_populates="tags", link_model=TagNote)


class TagGet(TagBase):
    id: int
    created_at: datetime


class TagGetWithNotes(TagGet):
    notes: list["NoteGet"] = []


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


from app.database.models.note import Note, NoteGet

TagGetWithNotes.update_forward_refs()
