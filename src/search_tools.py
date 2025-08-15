from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS  # Updated import for v8.x
from .utils import log_error

class WebSearchTool:
    """Tool for performing and processing web searches."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.headers = {
            "User-Agent": "FactCheckerBot/1.0"
        }

    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Perform web search and return processed results."""
        try:
            if self.api_key:
                # Use paid API if available
                return self._search_with_api(query, num_results)
            else:
                # Fallback to DuckDuckGo
                return self._search_with_ddg(query, num_results)
        except Exception as e:
            log_error(f"Search failed for '{query}': {str(e)}")
            return []

    def _search_with_api(self, query: str, num_results: int) -> List[Dict]:
        """Search using a commercial API (e.g., SerpAPI)."""
        params = {
            "q": query,
            "api_key": self.api_key,
            "num": num_results
        }
        
        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            headers=self.headers
        )
        response.raise_for_status()
        
        return self._process_api_results(response.json())

    def _search_with_ddg(self, query: str, num_results: int) -> List[Dict]:
        """Search using DuckDuckGo fallback (updated for v8.x)."""
        results = []
        try:
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=num_results):
                    results.append(r)
        except Exception as e:
            log_error(f"DuckDuckGo search error: {e}")
            return []
        return self._process_ddg_results(results)

    def _process_api_results(self, data: Dict) -> List[Dict]:
        """Process results from commercial API."""
        processed = []
        for result in data.get("organic_results", [])[:5]:
            processed.append({
                "title": result.get("title"),
                "url": result.get("link"),
                "snippet": result.get("snippet"),
                "domain": self._extract_domain(result.get("link"))
            })
        return processed

    def _process_ddg_results(self, results: List[Dict]) -> List[Dict]:
        """Process DuckDuckGo results."""
        processed = []
        for result in results:
            processed.append({
                "title": result.get("title"),
                "url": result.get("href"),
                "snippet": result.get("body"),
                "domain": self._extract_domain(result.get("href"))
            })
        return processed

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        if not url:
            return ""
        return url.split('/')[2] if '//' in url else url.split('/')[0]
