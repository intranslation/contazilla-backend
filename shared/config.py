from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/contab_hub"
    jwt_secret: str = "your-super-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 360

    # Boto3 Configuration
    r2_endpoint: str = ""
    r2_bucket: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    region_name: str = "auto"

    max_file_size_in_mb: int = 15

    class Config:
        env_file = ".env"


settings = Settings()
