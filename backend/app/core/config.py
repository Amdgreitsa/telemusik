from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    app_name: str = 'TeleMusik API'
    env: str = 'production'
    database_url: str = "sqlite+pysqlite:///:memory:"
    redis_url: str = "redis://localhost:6379/0"
    lastfm_api_key: str = "dev"
    lastfm_api_secret: str = "dev"
    apk_base_path: str = '/var/www/app/releases'
    jwt_secret: str = "dev-secret"


settings = Settings()
