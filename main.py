from src.fact_checker import FactChecker

def main():
    print("🏁 Fact-Checker Bot (Groq)")
    claim = input("Enter claim: ")
    
    result = FactChecker().fact_check(claim)
    print(f"\n🔎 Verdict: {result['verdict']}")
    print(f"\n📝 Report:\n{result['report']}")

if __name__ == "__main__":
    main()