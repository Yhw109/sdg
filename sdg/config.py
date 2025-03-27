from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, computed_field

class Settings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "sdg"

    @computed_field
    @property
    def DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=f"{self.POSTGRES_DB}"
        )

    MINIO_USERNAME: str = 'root'
    MINIO_PASSWORD: str = 'rootroot'
    MINIO_ENDPOINT: str = 'http://localhost:9001'

settings = Settings()
