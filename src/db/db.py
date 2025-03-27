from typing import Annotated, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from src.conf.app_settings import settings


class Movies(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    genre: str
    sensitive: Optional[bool] = False


movie_1 = Movies(name="Fight Club", genre="Thriller",sensitive=True)

db_user = f"{settings.db_settings.user}"
db_password = f"{settings.db_settings.password}"
db_host = f"{settings.db_settings.host}"
db_port = f"{settings.db_settings.port}"
db_name = f"{settings.db_settings.name}"

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")


SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(movie_1)
    session.commit()