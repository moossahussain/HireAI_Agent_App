import os
from pydantic_settings import BaseSettings 

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")
    
    # Model Configuration
    OPENAI_MODEL_NAME: str = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
    
    # API Configuration
    API_KEY: str = os.getenv("API_KEY", "")
    
    # Data paths
    RESUME_DIR: str = "data/resumes"
    OUTPUT_DIR: str = "data/outputs"
    
    class Config:
        env_file = ".env"

# Create a global settings object
settings = Settings()

# Set environment variables for CrewAI
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["OPENAI_MODEL_NAME"] = settings.OPENAI_MODEL_NAME
os.environ["SERPER_API_KEY"] = settings.SERPER_API_KEY