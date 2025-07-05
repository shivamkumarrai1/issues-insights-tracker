from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:Shivam%40sql@localhost:5432/tracker"
    SECRET_KEY: str = "super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    FRONTEND_ORIGIN: str = "http://localhost:5173"

settings = Settings()
