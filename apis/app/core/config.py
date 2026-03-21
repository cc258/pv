from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME:str = "PV"
    DATABASE:str = ""
    API_V1:str = "/api/v1"
    DEBUG:bool = True
    JWT:str = ""
    ALLOWED_ORIGINS:str = "*"
    APIKEY:str = ""

    class Config:
        env_file = "apis/.env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()