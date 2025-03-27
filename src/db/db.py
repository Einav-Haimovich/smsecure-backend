from sqlmodel import Session, SQLModel, create_engine, Field
from src.conf.app_settings import settings
from src.models.message import Message

db_user = f"{settings.db_settings.user}"
db_password = f"{settings.db_settings.password}"
db_host = f"{settings.db_settings.host}"
db_port = f"{settings.db_settings.port}"
db_name = f"{settings.db_settings.name}"
db_connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(db_connection_string)

def get_session():
    with Session(engine) as session:
        yield session