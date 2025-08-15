import unittest
from unittest.mock import patch, MagicMock
from src.fact_checker import FactChecker

class TestFactChecker(unittest.TestCase):
    @patch('src.fact_checker.ChatOpenAI')
    @patch('src.fact_checker.WebSearchTool')
    def setUp(self, mock_search, mock_llm):
        self.mock_llm = mock_llm
        self.mock_search = mock_search
        self.checker = FactChecker(openai_api_key="test_key")
        
    def test_initial_response(self):
        with patch.object(self.checker.initial_response_chain, 'run', return_value="Test response"):
            result = self.checker._get_initial_response("Test claim")
            self.assertEqual(result, "Test response")
            
    def test_assumption_extraction(self):
        test_response = "Claim 1\nClaim 2\nClaim 3"
        with patch.object(self.checker.assumption_extraction_chain, 'run', return_value=test_response):
            result = self.checker._extract_assumptions("Test input")
            self.assertEqual(len(result), 3)
            
    def test_claim_classification(self):
        with patch.object(self.checker, '_classify_claim', return_value="Factual"):
            result = self.checker.fact_check("Test claim")
            self.assertEqual(result["claim_type"], "Factual")

if __name__ == '__main__':
    unittest.main()