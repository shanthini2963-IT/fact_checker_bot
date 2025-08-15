import os
import sys
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent / "src"))

from fact_checker import FactChecker

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

st.markdown("""
<style>
/* Bigger input text */
.stTextArea textarea {
    font-size: 28px !important;
    line-height: 1.5 !important;
}

/* Bigger markdown output */
.stMarkdown p {
    font-size: 28px !important;
}

/* Headings */
h1, h2, h3, h4 {
    font-size: 34px !important;
}
</style>
""", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Fact-Checker", layout="wide")
    st.title("🔍 AI Fact-Checker Bot")

    # Claim input
    claim = st.text_area(
        " ",
        placeholder="Type your claim here...",
        height=150
    )

    if st.button("Verify") and claim:
        with st.spinner("Analyzing..."):
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

                st.header("📝 Claim to Verify")
                st.write(result.get("claim", "No claim provided."))
                st.write(f"Category: {result.get('claim_type', 'Unknown')}")

                st.subheader("📊 Final Verdict")
                if verdict == "true":
                    st.success("✅ True")
                elif verdict == "false":
                    st.error("❌ False")
                else:
                    st.warning("⚠️ Uncertain")

                st.subheader("📝 Summary")
                st.write(summary_text or "No summary available.")

                st.subheader("🔗 Key Evidence")
                key_evidence = result.get("final_answer", {}).get("key_evidence", [])
                if key_evidence:
                    for item in key_evidence:
                        st.markdown(f"- [{item.get('title','No title')}]({item.get('url','#')})")
                else:
                    st.write("No key evidence available.")

                st.subheader("📌 Assumptions & Verification")
                verification_results = result.get("verification_results", {})
                if verification_results:
                    for assumption, data in verification_results.items():
                        st.write(f"**{assumption}** — {data.get('verdict', 'Unknown')}")
                else:
                    st.write("No assumptions verified.")

                with st.expander("Show Detailed Analysis"):
                    st.json(result)

            except Exception as e:
                st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    if not groq_key:
        st.error("❌ Missing GROQ_API_KEY in .env file.")
    else:
        main()
