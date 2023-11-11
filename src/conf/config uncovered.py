from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_DB: str = 'rest_app'
    POSTGRES_USER: str = 'postgres'
    POSGRES_PASSWORD: str = '567234'
    POSTGRES_PORT: str = '5432'
    DATABASE_URL: str = f'postgresql+psycopg2://{POSTGRES_USER}:{POSGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}'
    secret_key: str = 'Some_key'
    algorithm: str = 'HS256'
    mail_username: str = 'amarakheo@meta.ua'
    mail_password: str = 'P0ldGpFDgDhLoxw4dKEH'
    mail_from: str = 'amarakheo@meta.ua'
    mail_port: int = 465
    mail_server: str = 'smtp.meta.ua'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str = 'dyhagw1bu'
    cloudinary_api_key: str = '922786134533285'
    cloudinary_api_secret: str = 'jA4_DPJdpZB9qQergmWhB8_8E_o'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()