from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME:str = "PV"
    DATABASE:str = ""
    API_PREFIX:str = "/api"
    DEBUG:bool = True
    JWT:str = ""
    ALLOWED_ORIGINS:str = "*"
    APIKEY:str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()