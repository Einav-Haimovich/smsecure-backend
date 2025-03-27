from sqlmodel import SQLModel, Field
from typing import Optional


class MessageBase(SQLModel):
    content: str = Field(index=True)
    sender: str = Field(index=True)
    time: str = Field(index=True)

class MessageCreate(MessageBase):
    score: Optional[float] = Field(default=None)


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    score: Optional[float] = Field(default=None)


class MessagePublic(MessageBase):
    id: int
    score: float
