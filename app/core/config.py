import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Global application configurations and environment variables loader.
    """
    PROJECT_NAME: str = "CogniMesh"
    API_V1_STR: str = "/api/v1"
    
    # LLM Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Model selection (defaulting to a robust model)
    DEFAULT_MODEL_NAME: str = os.getenv("DEFAULT_MODEL_NAME", "gemini-2.5-flash")

settings = Settings()