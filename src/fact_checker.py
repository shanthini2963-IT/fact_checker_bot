import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from groq import Groq

# Add src directory to path for module imports
sys.path.append(str(Path(__file__).parent))

from src.prompt_chains import (
    INITIAL_RESPONSE_TEMPLATE,
    ASSUMPTION_EXTRACTION_TEMPLATE, 
    VERIFICATION_TEMPLATE,
    FINAL_SYNTHESIS_TEMPLATE
)
from src.search_tools import WebSearchTool
from src.utils import log_error, validate_claim

class FactChecker:
    """Main fact-checking class using Groq API."""

    def __init__(self, groq_api_key: str, search_api_key: Optional[str] = None):
        """
        Initialize fact checker with Groq API.
        
        Args:
            groq_api_key: Groq API key
            search_api_key: Optional search API key (SerpAPI, etc.)
        """
        self.client = Groq(api_key=groq_api_key)
        self.search_tool = WebSearchTool(api_key=search_api_key)
        self.model = "openai/gpt-oss-20b"  # Groq's fastest model

        # Credibility scoring
        self.domain_scores = {
            '.gov': 0.9, '.edu': 0.85, '.org': 0.8,
            '.com': 0.7, '.net': 0.6, 'other': 0.5
        }

    def fact_check(self, claim: str) -> Dict[str, Any]:
        """
        Full fact-checking pipeline.
        
        Returns:
            {
                "claim": str,
                "claim_type": str,
                "initial_response": str,
                "assumptions": List[str],
                "verification_results": Dict,
                "final_answer": Dict,
                "status": str
            }
        """
        try:
            if not validate_claim(claim):
                return {"error": "Invalid claim", "status": "error"}

            # Step 1: Initial response
            initial = self._get_initial_response(claim)
            
            # Step 2: Extract assumptions
            assumptions = self._extract_assumptions(initial)
            
            # Step 3: Verify assumptions
            verification = self._verify_assumptions(assumptions)
            
            # Step 4: Final synthesis
            final = self._synthesize_final(claim, initial, verification)
            
            # Step 5: Classify claim
            claim_type = self._classify_claim(claim)

            return {
                "claim": claim,
                "claim_type": claim_type,
                "initial_response": initial,
                "assumptions": assumptions,
                "verification_results": verification,
                "final_answer": final,
                "status": "success"
            }

        except Exception as e:
            log_error(f"Fact-check failed: {str(e)}")
            return {"error": str(e), "status": "error"}

    def _query_groq(self, prompt: str) -> str:
        """Execute query against Groq API."""
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            log_error(f"Groq query failed: {str(e)}")
            raise

    def _get_initial_response(self, claim: str) -> str:
        """Generate preliminary assessment."""
        prompt = INITIAL_RESPONSE_TEMPLATE.format(claim=claim)
        return self._query_groq(prompt)

    def _extract_assumptions(self, text: str) -> List[str]:
        """Extract verifiable claims."""
        prompt = ASSUMPTION_EXTRACTION_TEMPLATE.format(response=text)
        result = self._query_groq(prompt)
        return [line.strip() for line in result.split('\n') if line.strip()]

    def _verify_assumptions(self, assumptions: List[str]) -> Dict[str, Dict]:
        """Verify each assumption with evidence."""
        results = {}
        
        for assumption in assumptions:
            try:
                # Get evidence
                evidence = self.search_tool.search(assumption)
                
                # Analyze
                prompt = VERIFICATION_TEMPLATE.format(
                    assumption=assumption,
                    evidence=evidence
                )
                analysis = self._query_groq(prompt)
                
                # Parse verdict (e.g., "Verdict: True")
                verdict = "Uncertain"
                if "Verdict:" in analysis:
                    verdict = analysis.split("Verdict:")[1].split("\n")[0].strip()
                
                results[assumption] = {
                    "verdict": verdict,
                    "evidence": evidence,
                    "credibility": self._score_credibility(evidence),
                    "analysis": analysis
                }
                
            except Exception as e:
                log_error(f"Failed to verify '{assumption}': {str(e)}")
                results[assumption] = {
                    "verdict": "Error",
                    "error": str(e)
                }
        
        return results

    def _synthesize_final(self, claim: str, initial: str, verification: Dict) -> Dict:
        """Generate final report."""
        prompt = FINAL_SYNTHESIS_TEMPLATE.format(
            claim=claim,
            initial_response=initial,
            verification_results=str(verification)
        )
        result = self._query_groq(prompt)
        
        # Parse structured response
        return {
            "verdict": self._parse_verdict(result),
            "summary": result,
            "confidence": self._estimate_confidence(result)
        }

    def _classify_claim(self, claim: str) -> str:
        """Classify claim type."""
        prompt = f"""Classify this claim:
        Categories: Factual, Opinion, Mixed, Unverifiable
        
        Claim: {claim}
        Category:"""
        return self._query_groq(prompt).strip()

    def _score_credibility(self, sources: List[Dict]) -> float:
        """Calculate average source credibility."""
        if not sources:
            return 0.0
            
        scores = []
        for source in sources:
            domain = source.get('domain', 'other')
            score = self.domain_scores.get(
                '.' + domain.split('.')[-1], 
                self.domain_scores['other']
            )
            scores.append(score)
        
        return round(sum(scores) / len(scores), 2)

    def _parse_verdict(self, text: str) -> str:
        """Extract verdict from final report."""
        text = text.lower()
        if "true" in text and "false" not in text:
            return "True"
        elif "false" in text:
            return "False"
        return "Uncertain"

    def _estimate_confidence(self, text: str) -> str:
        """Estimate confidence level."""
        text = text.lower()
        if "high confidence" in text:
            return "High"
        elif "medium confidence" in text:
            return "Medium"
        return "Low"