from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    log_level: str = "INFO"

    db_user: str = "nnergix_user"
    db_password: str
    db_host: str = "db"
    db_port: int = 5432
    db_name: str = "nnergix_db"

    https_proxy: str | None = None
    http_proxy: str | None = None
    no_proxy: str | None = None

    @property
    def postgresql_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()