from pathlib import Path

from pydantic import BaseConfig
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    name: str

    class Config:
        env_file = Path(__file__).parent.parent / '.env'
        env_prefix = 'db_'
        validate_assignment = True

    @property
    def url(self) -> str:
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


class Settings(BaseConfig):
    title: str = 'TaskTracker API'
    project_version: str = '0.1.0'
    project_description: str = 'TaskTracker API is a FastAPI-based REST API for managing tasks and employees'

    env: str = 'dev'
    port: int = 8000

    db: DBSettings = DBSettings()

    @property
    def debug(self) -> bool:
        return self.env == 'dev'

    class Config:
        env_file = Path(__file__).parent.parent / '.env'
        env_prefix = 'api_'
        validate_assignment = True


settings = Settings()
