import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "数码网购平台"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # 数据库 - Railway 使用 /app/data 持久化存储
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite://./shop.db")
    
    # JWT配置 - 生产环境必须设置环境变量
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
    
    # CORS - 生产环境设置具体域名
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")
    
    class Config:
        env_file = ".env"

settings = Settings()
