from sqlalchemy import Select
from sqlmodel import Session, SQLModel
from typing import Union, Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Depends, Query
from src.db.db import get_session, engine
from contextlib import asynccontextmanager

from src.models.message import Message


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up")
    SQLModel.metadata.create_all(engine)
    yield
    print("Application shutting down")


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(lifespan=lifespan)
@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/messages/")
async def get_messages(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Message]:
    messages = session.exec(Select(Message).offset(offset).limit(limit)).all()
    return messages

@app.post("/messages/")
async def create_message(message: Message, session: SessionDep) -> Message:
    print("im here")
    session.add(message)
    session.commit()
    session.refresh(message)
    return message