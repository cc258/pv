from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME:str = "PV"
    DATABASE:str = "sqlite:///./database.db"
    API_V1:str = "/api/v1"
    DEBUG:bool = True
    JWT:str = ""
    ALLOWED_ORIGINS:str = "*"
    APIKEY:str = ""

    TMDB_TOKEN:str = ""
    TMDB_KEY:str = ""
    TMDB_BASE:str = ""

    class Config:
        env_file = "backend/.env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()