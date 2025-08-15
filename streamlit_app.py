import os
import sys
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

# Import FactChecker
sys.path.append(str(Path(__file__).parent / "src"))
from src.fact_checker import FactChecker

# Load API key
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

# -------------------- Dark Professional Styling --------------------
st.set_page_config(page_title="AI Fact Checker", layout="wide")

st.markdown("""
<style>
/* General page background */
.stApp {
    background-color: #0e1117;
    font-family: 'Segoe UI', sans-serif;
    color: #e0e0e0;
}

/* Centered big title */
h1 {
    text-align: center;
    font-size: 40px !important;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 26px;
    color: #9aa0a6;
    margin-bottom: 25px;
}

/* Text input */
.stTextArea textarea {
    font-size: 26px !important;
    border-radius: 8px !important;
    padding: 10px !important;
    border: 1px solid #3c4043 !important;
    background-color: #1c1f26 !important;
    color: #f5f5f5 !important;
}

/* Buttons */
.stButton button {
    background-color: #1a73e8 !important;
    color: white !important;
    font-size: 26px !important;
    border-radius: 6px !important;
    padding: 8px 18px !important;
    font-weight: 500;
    border: none;
    transition: 0.2s ease;
}
.stButton button:hover {
    background-color: #1558b0 !important;
}

/* Section headers */
h2, h3, h4 {
    color: #e8eaed !important;
    font-weight: 600;
}

/* Verdict highlight boxes */
div[data-testid="stSuccess"] {
    border-left: 6px solid #34a853;
    background-color: rgba(52, 168, 83, 0.1);
}
div[data-testid="stError"] {
    border-left: 6px solid #ea4335;
    background-color: rgba(234, 67, 53, 0.1);
}
div[data-testid="stWarning"] {
    border-left: 6px solid #fbbc05;
    background-color: rgba(251, 188, 5, 0.1);
}

/* Card-like sections */
.card {
    background-color: #1a1d23;
    padding: 15px 20px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- Main App --------------------
def main():
    st.title("AI Fact Checker Bot")
    st.markdown("<div class='subtitle'>verify claims using AI-powered research and analysis</div>", unsafe_allow_html=True)

    claim = st.text_area(
        " ",
        placeholder="Enter your claim",
        height=120
    )

    if st.button("Verify") and claim:
        with st.spinner("Analyzing claim..."):
            try:
                checker = FactChecker(groq_api_key=groq_key)
                result = checker.fact_check(claim)

                verdict = result.get("final_answer", {}).get("verdict", "").lower()
                summary_text = (
                    result.get("final_answer", {}).get("summary_short")
                    or result.get("final_answer", {}).get("summary")
                    or ""
                )

                if "not visible" in summary_text.lower() or "false" in summary_text.lower():
                    verdict = "false"

                st.markdown("---")

                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("📝 Claim to Verify")
                st.info(result.get("claim", "No claim provided."))
                st.write(f"**Category:** {result.get('claim_type', 'Unknown')}")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("📊 Final Verdict")
                if verdict == "true":
                    st.success("✅ True")
                elif verdict == "false":
                    st.error("❌ False")
                else:
                    st.warning("⚠️ Uncertain")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("📝 Summary")
                st.write(summary_text or "No summary available.")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("🔗 Key Evidence")
                key_evidence = result.get("final_answer", {}).get("key_evidence", [])
                if key_evidence:
                    for item in key_evidence:
                        st.markdown(f"🔹 [{item.get('title','No title')}]({item.get('url','#')})")
                else:
                    st.write("No key evidence available.")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("📌 Assumptions & Verification")
                verification_results = result.get("verification_results", {})
                if verification_results:
                    for assumption, data in verification_results.items():
                        verdict_text = data.get('verdict', 'Unknown')
                        st.write(f"**{assumption}** — {verdict_text}")
                else:
                    st.write("No assumptions verified.")
                st.markdown("</div>", unsafe_allow_html=True)

                with st.expander("📂 Show Detailed Analysis"):
                    st.json(result)

            except Exception as e:
                st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    if not groq_key:
        st.error("❌ Missing GROQ_API_KEY in .env file.")
    else:
        main()
