from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    EXTERNAL_API_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
