import streamlit as st
import pandas as pd
import random

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Benefits Choice Coach", page_icon="💬", layout="wide")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #f6f9fc, #ffffff);
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        background: #ffffffcc;
        padding: 2rem 4rem;
        border-radius: 20px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.08);
        backdrop-filter: blur(8px);
    }
    h1, h2, h3 {
        color: #15395b;
    }
    .stButton>button {
        background: linear-gradient(90deg, #003366, #0072bb);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #0072bb, #0094d4);
    }
    .chat-bubble-user {
        background: #e9f3ff;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 8px 0;
        max-width: 80%;
        animation: fadeIn 0.5s;
    }
    .chat-bubble-bot {
        background: #fff7e6;
        border-left: 5px solid #f5b800;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 8px 0;
        max-width: 85%;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    [data-testid="stSidebar"] {
        background-color: #0d294d;
        color: #ffffff;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- APP HEADER --------------------
st.title("💬 Benefits Choice Coach")
st.markdown("### ✨ Your Personal AI Advisor for HR Benefits")
st.write("Helping you choose the right health, life, and insurance plan — stress-free.")

# -------------------- SIDEBAR --------------------
st.sidebar.header("🧍 Employee Profile")
age = st.sidebar.slider("Age", 18, 65, 30)
family = st.sidebar.selectbox("Family Status", ["Single", "Married", "With Children"])
risk = st.sidebar.select_slider("Risk Tolerance", ["Low", "Medium", "High"], value="Medium")
income = st.sidebar.number_input("Monthly Income (USD)", 2000, 20000, 5000, step=100)
st.sidebar.markdown("---")

# -------------------- CHATBOT SECTION --------------------
st.subheader("🤖 Chat with Benefits Coach")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "bot", "text": "Hello 👋 I'm your Benefits Coach. Ask me about health, insurance, or plan recommendations!"}
    ]

user_input = st.text_input("You:", placeholder="Ask something like 'Which plan is good for families?'")

# --- Demo Chat Logic ---
def get_demo_reply(text):
    text = text.lower()
    if "recommend" in text or "best" in text or "choose" in text:
        if risk == "Low":
            return "Based on your **Low risk tolerance**, I recommend **Plan A (Low Cost)** — minimal coverage, minimal cost."
        elif risk == "Medium":
            return "For your **Medium risk tolerance**, **Plan B (Balanced)** is a great choice — balanced coverage and cost."
        else:
            return "With your **High risk tolerance**, you should explore **Plan C (Comprehensive)** — premium coverage, full protection."
    elif "cost" in text or "price" in text:
        return "💲 Plan A: $150/month | Plan B: $250/month | Plan C: $400/month."
    elif "health" in text or "insurance" in text:
        return "Health insurance covers doctor visits, hospitalization, and preventive care. Want to compare plans?"
    elif "family" in text:
        return "For families, **Plan C** is usually preferred — it includes wider coverage for dependents."
    elif "hello" in text or "hi" in text:
        return "👋 Hi there! I'm here to help you navigate your benefits easily."
    else:
        return "🤔 Sorry, I don’t have an answer for that — but you can ask about plan cost, recommendation, or coverage!"

# --- Chat Handling ---
if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    reply = get_demo_reply(user_input)
    st.session_state.chat_history.append({"role": "bot", "text": reply})

# --- Display Chat History ---
for msg in st.session_state.chat_history:
    if msg["role"] == "bot":
        st.markdown(f"<div class='chat-bubble-bot'><b>Coach:</b> {msg['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-user'><b>You:</b> {msg['text']}</div>", unsafe_allow_html=True)

# -------------------- PLAN SIMULATION --------------------
st.subheader("📊 Plan Comparison Simulator")

data = pd.DataFrame({
    "Plan": ["Plan A", "Plan B", "Plan C"],
    "Monthly Cost": [150, 250, 400],
    "Coverage Score": [60, 80, 95],
    "Satisfaction (Simulated)": [random.randint(60, 95) for _ in range(3)]
})

st.dataframe(data)
st.bar_chart(data.set_index("Plan")["Monthly Cost"])

# -------------------- LEARNING CENTER --------------------
with st.expander("📘 Learn About Each Benefit"):
    st.markdown("""
    **Health Insurance:** Covers doctor visits, hospitalization, and preventive care.  
    **Life Insurance:** Protects your family financially in case of unexpected events.  
    **Dental & Vision:** Optional add-ons for dental and eye care.  
    **FSA (Flexible Spending Account):** Save pre-tax money for health expenses.
    """)

# -------------------- AUTO PLAN RECOMMENDATION LOGIC --------------------
def recommend_plan_auto(risk_level, income_level):
    if risk_level == "Low":
        if income_level < 4000:
            return "Plan A (Low Cost)"
        else:
            return "Plan B (Balanced)"
    elif risk_level == "Medium":
        if income_level < 5000:
            return "Plan B (Balanced)"
        else:
            return "Plan C (Comprehensive)"
    else:  # High risk
        return "Plan C (Comprehensive)"

recommended_plan = recommend_plan_auto(risk, income)

# -------------------- SUMMARY SECTION --------------------
st.subheader("📝 Personalized Summary Sheet (Demo)")

summary = f"""
### Benefits Summary for {family} ({age} years old)
- **Risk Tolerance:** {risk}
- **Monthly Income:** ${income}
- **Recommended Plan:** {recommended_plan}
"""

st.markdown(summary)
st.download_button("💾 Download Summary (Demo)", summary.encode(), "Benefits_Summary.txt")

st.markdown("---")
st.caption("© 2025 Benefits Choice Coach | Prototype by HR Innovation Lab")
