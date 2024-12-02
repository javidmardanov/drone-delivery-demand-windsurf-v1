"""Download and process taginfo database."""
import os
import bz2
import sqlite3
import requests
from typing import List, Dict, Any
from .config import Config

class TagInfoDownloader:
    """Download and process taginfo database."""
    
    def __init__(self):
        Config.ensure_directories()
        
    def download_database(self) -> None:
        """Download the taginfo wiki database."""
        if os.path.exists(Config.TAGINFO_DB_PATH):
            print("Database already exists.")
            return
            
        print("Downloading taginfo wiki database...")
        response = requests.get(Config.TAGINFO_WIKI_URL, stream=True)
        response.raise_for_status()
        
        # Download and decompress in chunks
        compressed_path = f"{Config.TAGINFO_DB_PATH}.bz2"
        with open(compressed_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print("Decompressing database...")
        with bz2.open(compressed_path, 'rb') as source, open(Config.TAGINFO_DB_PATH, 'wb') as target:
            target.write(source.read())
            
        os.remove(compressed_path)
        print("Download complete.")
        
    def get_tags(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get tags from the database with their descriptions.
        
        Args:
            limit: Maximum number of tags to return.
            
        Returns:
            List of dictionaries containing tag information.
        """
        if not os.path.exists(Config.TAGINFO_DB_PATH):
            raise FileNotFoundError("Database not found. Run download_database() first.")
            
        conn = sqlite3.connect(Config.TAGINFO_DB_PATH)
        cursor = conn.cursor()
        
        query = """
        SELECT DISTINCT k.key, k.description
        FROM wiki_keys k
        WHERE k.description IS NOT NULL
        LIMIT ?
        """
        
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        
        tags = []
        for key, description in results:
            tags.append({
                "key": key,
                "description": description
            })
            
        conn.close()
        return tags
