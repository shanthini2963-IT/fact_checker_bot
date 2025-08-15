import os
from groq import Groq
from typing import Dict, Any

class GroqClient:
    """Lightweight Groq API client with error handling."""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def query(self, prompt: str, model: str = "mixtral-8x7b-32768") -> Dict[str, Any]:
        """Run a single LLM query."""
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                temperature=0.3
            )
            return {
                "success": True,
                "output": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }