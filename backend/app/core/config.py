from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME:str = "PV"
    DATABASE:str = "sqlite:///./database.db"
    API_V1:str = "/apis/v1"
    DEBUG:bool = True
    SECRET_KEY:str = ""
    ALLOWED_ORIGINS:str = "*"
    APIKEY:str = ""

    DUMMY_HASH:str = ""

    class Config:
        env_file = "backend/.env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()