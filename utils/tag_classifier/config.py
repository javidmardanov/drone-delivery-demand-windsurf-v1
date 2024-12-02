"""Configuration for tag classifier."""
import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

class TagCategory(Enum):
    ORIGIN = "origin"
    DESTINATION = "destination"
    NONE = "none"

@dataclass
class AIConfig:
    """Configuration for AI models."""
    model_name: str
    temperature: float = 0.3
    max_tokens: int = 150

class Config:
    """Global configuration."""
    # Data paths
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    TAGINFO_DB_PATH = os.path.join(DATA_DIR, "taginfo-wiki.db")
    CLASSIFICATION_CACHE_PATH = os.path.join(DATA_DIR, "tag_classifications.json")
    
    # Download URLs
    TAGINFO_WIKI_URL = "https://taginfo.openstreetmap.org/download/taginfo-wiki.db.bz2"
    
    # AI Models
    OPENAI_MODEL = AIConfig(model_name="gpt-4")
    OLLAMA_MODEL = AIConfig(model_name="mistral")
    
    # Batch processing
    BATCH_SIZE = 100
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all necessary directories exist."""
        os.makedirs(cls.DATA_DIR, exist_ok=True)
