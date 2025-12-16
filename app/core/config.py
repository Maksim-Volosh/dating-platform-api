from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    
class DetailsConfig(BaseModel):
    title: str = "FastAPI App"
    description: str = "API"
    
class ApiConfig(BaseModel):
    prefix: str = "/api"
    
class SecurityConfig(BaseModel):
    api_key: str
    
class StaticFilesConfig(BaseModel):
    directory: str = "./uploads"
    url: str = "/uploads"

class DatabaseConfig(BaseSettings):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    
class CacheConfig(BaseSettings):
    url: str
    
class DeckConfig(BaseSettings):
    timeout: int = 60 * 60
    max_size: int = 100
    
class InboxConfig(BaseSettings):
    timeout: int = 604800

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    security: SecurityConfig
    api: ApiConfig = ApiConfig()
    db: DatabaseConfig
    cache: CacheConfig
    static: StaticFilesConfig = StaticFilesConfig()
    details: DetailsConfig = DetailsConfig()
    deck: DeckConfig = DeckConfig()
    inbox: InboxConfig = InboxConfig()
    

settings = Settings() # type: ignore