# 🕵️‍♂️ Fact Checker Bot

A **Streamlit-based web application** that verifies the truthfulness of any statement using the **Groq API** and language models.  
This tool is designed to quickly check whether a claim is true, false, or unverifiable — ideal for research, journalism, and general fact-checking.

---

## 📌 Features
- ✅ **Claim Verification** – Enter any statement and receive an AI-based truth assessment.  
- 🌐 **Live Data Retrieval** – Cross-checks with trusted sources for better accuracy.  
- 📊 **Detailed Analysis** – Displays verification results, explanation, and confidence score.  
- 🎨 **Professional Dark-Themed UI** – Sleek black background with light-colored text for modern look.  
- 📷 **Screenshot-ready Dashboard** – Perfect for portfolio and demo purposes.

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/fact_checker_bot.git
   cd fact_checker_bot
````

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Groq API Key**
   Create a `.env` file in the project root and add:

   ```env
   GROQ_API_KEY=your_api_key_here
   ```

4. **Run the application**

   ```bash
   streamlit run streamlit_app.py
   ```

---

## 📂 Project Structure

```
fact_checker_bot/
│── streamlit_app.py        # Main Streamlit dashboard
│── fact_checker.py         # FactChecker class for logic & API calls
│── requirements.txt        # Required Python packages
│── .env                    # API key storage
│── output/                 # Screenshots and saved results
│   ├── Sun-star 1.png
│   ├── knuckles 1.png
```

---

## 🖼️ Screenshots

### 🔹 Claim Verification Example – Knuckles

![Knuckles Example](output/knuckles%201.png)

### 🔹 Claim Verification Example – Sun and Star

![Sun-Star Example](output/Sun-star%201.png)

---

## ⚙️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **AI Model:** Groq API (Language Models)
* **Styling:** Streamlit Custom CSS (Dark Theme)

---

## 🧠 How It Works

1. **Input a claim** into the dashboard.
2. The **FactChecker** class sends the claim to the Groq API for analysis.
3. AI model evaluates and returns:

   * Truth assessment (True / False / Unverifiable)
   * Explanation with context
   * Confidence score
4. Results are displayed instantly in a **professional dark UI**.

---

## 🙌 Acknowledgments

* **Groq API** for providing AI inference capabilities
* **Streamlit** for making data apps simple and beautiful
```
