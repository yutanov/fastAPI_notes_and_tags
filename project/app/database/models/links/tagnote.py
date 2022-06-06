from typing import Optional

from sqlmodel import Field, SQLModel


class TagNote(SQLModel, table=True):
    __tablename__ = "tagnote_links"

    tag_id: Optional[int] = Field(
        default=None, foreign_key="tags.id", primary_key=True
    )
    note_id: Optional[int] = Field(
        default=None, foreign_key="notes.id", primary_key=True
    )
