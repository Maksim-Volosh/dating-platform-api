from pydantic_settings import BaseSettings
from pydantic import BaseModel


class RunConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    
class ApiConfig(BaseModel):
    api_prefix: str = "/api"

class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiConfig = ApiConfig()
    

settings = Settings()