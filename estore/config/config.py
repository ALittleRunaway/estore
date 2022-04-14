from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass
class DataBaseConfig:
    username: str
    password: str
    host: str
    db_name: str

@dataclass
class Config:
    db: DataBaseConfig


def initConfig() -> Config:
    load_dotenv()
    return Config(
        db=DataBaseConfig(
            username=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            db_name=os.getenv("DB_NAME"),
        )
    )
