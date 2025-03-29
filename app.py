from sqlalchemy import Select
from sqlmodel import Session, SQLModel, select
from typing import Union, Annotated, Sequence, List
from fastapi import FastAPI, Depends, Query, APIRouter

from src.db.db import get_session, engine
from contextlib import asynccontextmanager
from src.models.message import MessageBase, MessageCreate, MessagePublic, Message, MessageCreateBulk


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up")
    SQLModel.metadata.create_all(engine)
    yield
    print("Application shutting down")


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(lifespan=lifespan)
router = APIRouter()
@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/messages/",status_code=200 ,response_model=list[MessagePublic])
async def get_messages(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> List[MessagePublic]:
    messages = session.exec(select(Message).offset(offset).limit(limit)).all()
    return [MessagePublic.model_validate(m) for m in messages]

@app.post("/messages/", status_code=201, response_model=MessagePublic)
async def create_message(message: MessageCreate, session: SessionDep) -> Message:
    if not message.score:
        message.score = 50.0
    db_message = Message.model_validate(message)
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message

@app.post("/messages/bulk/", status_code=201, response_model=List[MessagePublic])
async def create_messages_bulk(
    request: MessageCreateBulk,
    session: SessionDep
) -> List[Message]:
    db_messages = []
    for message in request.messages:
        if not message.score:
            message.score = 50.0
        db_message = Message.model_validate(message)
        session.add(db_message)
        db_messages.append(db_message)

    session.commit()
    for msg in db_messages:
        session.refresh(msg)

    return db_messages