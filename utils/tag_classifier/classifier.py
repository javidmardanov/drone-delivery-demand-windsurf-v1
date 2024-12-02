"""Tag classifier using AI models."""
import json
import os
from typing import Dict, List, Optional
import openai
from openai import OpenAI
import requests
from .config import Config, TagCategory

class AIClassifier:
    """Base class for AI-based tag classification."""
    
    def __init__(self):
        self.cache = self._load_cache()
        
    def _load_cache(self) -> Dict:
        """Load cached classifications."""
        if os.path.exists(Config.CLASSIFICATION_CACHE_PATH):
            with open(Config.CLASSIFICATION_CACHE_PATH, 'r') as f:
                return json.load(f)
        return {}
        
    def _save_cache(self) -> None:
        """Save classifications to cache."""
        with open(Config.CLASSIFICATION_CACHE_PATH, 'w') as f:
            json.dump(self.cache, f, indent=2)
            
    def classify_tags(self, tags: List[Dict]) -> Dict[str, TagCategory]:
        """Classify a batch of tags."""
        raise NotImplementedError

class OpenAIClassifier(AIClassifier):
    """OpenAI-based tag classifier."""
    
    def __init__(self, api_key: str):
        super().__init__()
        self.client = OpenAI(api_key=api_key)
        self.config = Config.OPENAI_MODEL
        
    def classify_tags(self, tags: List[Dict]) -> Dict[str, TagCategory]:
        """Classify tags using OpenAI API."""
        results = {}
        uncached_tags = [tag for tag in tags if tag['key'] not in self.cache]
        
        if uncached_tags:
            prompt = self._create_prompt(uncached_tags)
            response = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that classifies OpenStreetMap tags."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Parse response and update cache
            classifications = self._parse_response(response.choices[0].message.content)
            self.cache.update(classifications)
            self._save_cache()
            
        # Combine cached and new results
        results = {**self.cache, **results}
        return {tag['key']: results.get(tag['key'], TagCategory.NONE.value) for tag in tags}
        
    def _create_prompt(self, tags: List[Dict]) -> str:
        """Create prompt for OpenAI API."""
        prompt = "Classify each OpenStreetMap tag as either 'origin', 'destination', or 'none' based on whether it typically represents:\n"
        prompt += "- origin: A place where people/goods typically start their journey\n"
        prompt += "- destination: A place where people/goods typically end their journey\n"
        prompt += "- none: Neither an origin nor a destination\n\n"
        prompt += "For each tag, respond with only the classification (origin/destination/none). Tags:\n\n"
        
        for tag in tags:
            prompt += f"Tag: {tag['key']}\nDescription: {tag['description']}\nClassification: "
            
        return prompt
        
    def _parse_response(self, response: str) -> Dict[str, str]:
        """Parse OpenAI response into classifications."""
        classifications = {}
        lines = response.strip().split('\n')
        current_tag = None
        
        for line in lines:
            line = line.strip().lower()
            if line.startswith('tag: '):
                current_tag = line[5:].strip()
            elif line.startswith('classification: '):
                if current_tag:
                    classification = line[15:].strip()
                    if classification in [cat.value for cat in TagCategory]:
                        classifications[current_tag] = classification
                    current_tag = None
                    
        return classifications

class OllamaClassifier(AIClassifier):
    """Ollama-based tag classifier."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        super().__init__()
        self.base_url = base_url
        self.config = Config.OLLAMA_MODEL
        
    def classify_tags(self, tags: List[Dict]) -> Dict[str, TagCategory]:
        """Classify tags using Ollama API."""
        results = {}
        uncached_tags = [tag for tag in tags if tag['key'] not in self.cache]
        
        if uncached_tags:
            prompt = self._create_prompt(uncached_tags)
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.config.model_name,
                    "prompt": prompt,
                    "temperature": self.config.temperature,
                }
            )
            response.raise_for_status()
            
            # Parse response and update cache
            classifications = self._parse_response(response.json()['response'])
            self.cache.update(classifications)
            self._save_cache()
            
        # Combine cached and new results
        results = {**self.cache, **results}
        return {tag['key']: results.get(tag['key'], TagCategory.NONE.value) for tag in tags}
        
    def _create_prompt(self, tags: List[Dict]) -> str:
        """Create prompt for Ollama API."""
        return OpenAIClassifier._create_prompt(self, tags)
        
    def _parse_response(self, response: str) -> Dict[str, str]:
        """Parse Ollama response into classifications."""
        return OpenAIClassifier._parse_response(self, response)
