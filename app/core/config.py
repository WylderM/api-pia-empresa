from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

env_file = ".env.test" if os.getenv("PYTEST_RUNNING") else ".env"
load_dotenv(env_file)

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    redis_url: str

    model_config = SettingsConfigDict(env_file=env_file)

settings = Settings()
