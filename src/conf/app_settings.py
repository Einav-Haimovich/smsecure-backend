from typing import Optional

from pathlib import Path
from pydantic import Field, EmailStr
from typing import Annotated
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

PathField = Annotated[Path, lambda x: Path(x)]

BooleanField = Annotated[
    bool, lambda x: x == "1" or x == "true" or x == "True" or x == True
]


def create_absolute_dir_path(dirname: str) -> Path:
    return Path.cwd() / dirname

class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="db_",
        cli_prefix="db_",
        env_file=".env",
        extra="ignore",
    )

    password: str = Field(
        default = "",
        description="The database password",
    )
    user: str = Field(
        default = "",
        description="The database user",
    )
    name: str = Field(
        default = "",
        description="The database name",
    )
    host: str = Field(
        default = "",
        description="The database host",
    )
    port: int = Field(
        default = 5432,
        description="The database port",
    )

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        validate_assignment=True,
        case_sensitive=False,
    )

    db_settings: DBSettings = DBSettings()

    env: str = Field(
        default="dev", title="The environment", description="The environment"
    )

    base_dir: PathField = Field(
        default_factory=lambda: Path.cwd(), description="The base directory"
    )

    debug: BooleanField = Field(default=False, description="Debug mode")

    logfile: Optional[PathField] = Field(
        default=None,
        description="The log file",
    )

    app_timezone: str = Field(default="Asia/Tel_Aviv", description="The app timezone")

    @property
    def is_dev(self) -> bool:
        return "dev" in self.env.lower()

    @property
    def is_prod(self) -> bool:
        return "prod" in self.env.lower()

    @property
    def is_test(self) -> bool:
        return "test" in self.env.lower()

    @property
    def is_staging(self) -> bool:
        return "staging" in self.env.lower()

    @property
    def static_dir(self) -> Path:
        return self.base_dir / "static"


settings: Settings = Settings()