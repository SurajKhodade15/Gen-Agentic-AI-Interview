from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_env: str = "local"
    log_level: str = "INFO"
    jwt_secret: str = "unsafe-local-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "enterprise_knowledge"
    redis_url: str = "redis://localhost:6379/0"
    redis_ttl_seconds: int = 3600
    rate_limit: str = "30/minute"
    s3_document_bucket: str = ""
    s3_quarantine_bucket: str = ""
    secrets_manager_secret_id: str = ""
    cognito_issuer: str = ""
    cognito_audience: str = ""
    allowed_origins: str = "http://localhost:3000"


@lru_cache
def get_settings() -> Settings:
    return Settings()
