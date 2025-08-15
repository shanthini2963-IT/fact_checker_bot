from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# =========================================
# String templates for direct .format() use
# =========================================

INITIAL_RESPONSE_TEMPLATE = """
[INST] You are a fact-checking assistant. Provide a concise preliminary answer to:
Claim: {claim}
[/INST]
Preliminary Answer:
"""

ASSUMPTION_EXTRACTION_TEMPLATE = """
Analyze this text and extract all factual claims that could be independently verified.
List each claim on a new line. Be specific.

Text: {response}
Verifiable Claims:
"""

VERIFICATION_TEMPLATE = """
Based on the provided evidence, determine if this assumption is:
- True (supported by evidence)
- False (contradicted by evidence)
- Uncertain (insufficient evidence)

Provide your verdict and reasoning.

Assumption: {assumption}
Evidence: {evidence}

Structure your response as:
Verdict: [True/False/Uncertain]
Reasoning: [Your analysis]
"""

FINAL_SYNTHESIS_TEMPLATE = """
Create a comprehensive fact-check report for this claim based on the verification results.
Include:
1. Final verdict (True/False/Mixed/Unverifiable)
2. Confidence level (Low/Medium/High)
3. Summary of findings
4. Key supporting/contradictory evidence

Claim: {claim}
Initial Assessment: {initial_response}
Verification Results: {verification_results}

Final Report:
"""

# =========================================
# LangChain-based chain builders (optional)
# =========================================

def get_initial_response_chain():
    """Chain for generating initial assessment."""
    template = INITIAL_RESPONSE_TEMPLATE
    return template  # Raw template, Groq handles formatting

def get_assumption_extraction_chain(llm):
    """Chain for extracting verifiable assumptions."""
    prompt = PromptTemplate.from_template(ASSUMPTION_EXTRACTION_TEMPLATE)
    return LLMChain(llm=llm, prompt=prompt)

def get_verification_chain(llm):
    """Chain for verifying assumptions against evidence."""
    prompt = PromptTemplate.from_template(VERIFICATION_TEMPLATE)
    return LLMChain(llm=llm, prompt=prompt)

def get_final_synthesis_chain(llm):
    """Chain for synthesizing final fact-check report."""
    prompt = PromptTemplate.from_template(FINAL_SYNTHESIS_TEMPLATE)
    return LLMChain(llm=llm, prompt=prompt)
