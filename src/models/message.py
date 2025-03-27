from sqlmodel import SQLModel, Field


class MessageBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(index=True)
    sender: str = Field(index=True)
    time: str = Field(index=True)

class Message(MessageBase,table=True):
    id: int | None = Field(default=None, primary_key=True)

class MessagePublic(MessageBase):
    id: int
    score: float
