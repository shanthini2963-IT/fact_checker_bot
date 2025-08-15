from src.fact_checker import FactChecker
import os

def display_result(result):
    """Display fact-check results in CLI."""
    print("\n" + "="*50)
    print(f"CLAIM: {result['claim']}")
    print(f"TYPE: {result.get('claim_type', 'Unknown')}")
    
    final = result["final_answer"]
    print(f"\nVERDICT: {final.get('verdict', 'Uncertain')}")
    print(f"CONFIDENCE: {final.get('confidence', 'Low')}")
    print(f"\nSUMMARY:\n{final.get('summary', 'No summary available.')}")
    
    print("\nASSUMPTIONS VERIFIED:")
    for assumption, details in result["verification_results"].items():
        print(f"\n• {assumption}")
        print(f"  Verdict: {details['verdict']}")
        print(f"  Credibility: {details['credibility']}")
        print(f"  Reasoning: {details['reasoning']}")
        
        print("  Sources:")
        for i, source in enumerate(details['sources'][:2], 1): 
            print(f"    {i}. {source['title']}")
            print(f"       {source['url']}")

def main():
    print("AI Fact-Checker Bot (CLI Version)")
    print("="*50)
    
    api_key = os.getenv("OPENAI_API_KEY") or input("Enter OpenAI API Key: ")
    search_key = os.getenv("SEARCH_API_KEY") or input("Enter Search API Key (optional, press Enter to skip): ")
    
    checker = FactChecker(openai_api_key=api_key, search_api_key=search_key)
    
    while True:
        print("\n" + "="*50)
        claim = input("Enter a claim to verify (or 'quit' to exit): ")
        
        if claim.lower() == 'quit':
            break
            
        print("\nVerifying claim...")
        result = checker.fact_check(claim)
        
        if "error" in result:
            print(f"\nError: {result['error']}")
        else:
            display_result(result)

if __name__ == "__main__":
    main()