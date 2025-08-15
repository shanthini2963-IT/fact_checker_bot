import logging
from typing import Union, List, Dict, Any
from pathlib import Path
import json

def setup_logging(log_file: str = "fact_checker.log") -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def log_error(message: str):
    print(f"ERROR: {message}")

def validate_claim(claim: str) -> bool:
    return isinstance(claim, str) and len(claim.strip()) > 0

def save_to_cache(data: Dict[str, Any], cache_file: str = "cache.json") -> bool:
    """
    Save data to a cache file.
    
    Args:
        data: Data to cache
        cache_file: Cache file path
        
    Returns:
        bool: True if successful
    """
    try:
        with open(cache_file, 'w') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        log_error(f"Cache save failed: {str(e)}")
        return False

def load_from_cache(cache_file: str = "cache.json") -> Union[Dict[str, Any], None]:
    """
    Load cached data.
    
    Args:
        cache_file: Cache file path
        
    Returns:
        dict or None: Cached data if exists
    """
    if not Path(cache_file).exists():
        return None
        
    try:
        with open(cache_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        log_error(f"Cache load failed: {str(e)}")
        return None

def clean_text(text: str) -> str:
    """
    Clean and normalize text for processing.
    
    Args:
        text: Input text to clean
        
    Returns:
        str: Cleaned text
    """
    if not isinstance(text, str):
        return ""
        
    text = text.strip()
    text = ' '.join(text.split())  
    return text

def calculate_credibility(sources: List[Dict[str, Any]]) -> float:
    """
    Calculate average credibility score for sources.
    
    Args:
        sources: List of source dictionaries
        
    Returns:
        float: Average credibility score (0.0-1.0)
    """
    if not sources:
        return 0.0
        
    domain_scores = {
        '.gov': 0.9, '.edu': 0.85, '.org': 0.8,
        '.com': 0.7, '.net': 0.6, 'other': 0.5
    }
    
    total = 0.0
    for source in sources:
        domain = source.get('domain', '').lower()
        score = domain_scores.get('.' + domain.split('.')[-1], domain_scores['other'])
        total += score
        
    return round(total / len(sources), 2)

# Initialize logging when module is imported
setup_logging()