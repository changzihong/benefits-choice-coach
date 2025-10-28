import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="Benefits Choice Coach", page_icon="💬", layout="wide")

# ---- CUSTOM STYLES ----
st.markdown("""
    <style>
    /* --- GLOBAL --- */
    body {
        background: linear-gradient(120deg, #f7f9fc, #ffffff);
        color: #1a1a1a;
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        padding: 2rem 4rem;
        background: #ffffffaa;
        border-radius: 20px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.08);
        backdrop-filter: blur(5px);
    }
    h1, h2, h3 {
        color: #1b3556;
    }
    .stButton>button {
        background: linear-gradient(90deg, #002b5c, #0072bb);
        color: white;
        border-radius: 10px;
        padding: 10px 25px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #0072bb, #0094d4);
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    /* --- CHAT BOX --- */
    .chat-bubble-user {
        background: #eaf4ff;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 8px 0;
        max-width: 80%;
        animation: fadeIn 0.8s;
    }
    .chat-bubble-bot {
        background: #fff7e6;
        border-left: 5px solid #f5b800;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 8px 0;
        max-width: 85%;
        animation: fadeIn 1s;
    }
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    /* --- SIDEBAR --- */
    [data-testid="stSidebar"] {
        background-color: #0d294d;
        color: #ffffff;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] select {
        border-radius: 8px;
        border: none;
        padding: 6px;
    }
    /* --- EXPANDER --- */
    .streamlit-expanderHeader {
        background-color: #f0f3fa;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---- OPTIONAL JAVASCRIPT EFFECTS ----
st.markdown("""
    <script>
    const fadeIn = (el, time) => {
        el.style.opacity = 0;
        let last = +new Date();
        const tick = () => {
            el.style.opacity = +el.style.opacity + (new Date() - last) / time;
            last = +new Date();
            if (+el.style.opacity < 1) {
                requestAnimationFrame(tick);
            }
        };
        tick();
    };

    window.addEventListener('load', () => {
        document.querySelectorAll('.chat-bubble-bot, .chat-bubble-user').forEach(el => fadeIn(el, 1000));
    });
    </script>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.title("💬 Benefits Choice Coach")
st.markdown("<h4>✨ Your AI-powered HR Benefits Advisor</h4>", unsafe_allow_html=True)
st.write("Simplify benefits enrollment with personalized guidance and cost simulations.")

# ---- SIDEBAR ----
st.sidebar.header("🧍 Employee Profile")
age = st.sidebar.slider("Age", 18, 65, 30)
family = st.sidebar.selectbox("Family Status", ["Single", "Married", "With Children"])
risk = st.sidebar.select_slider("Risk Tolerance", options=["Low", "Medium", "High"])
income = st.sidebar.number_input("Monthly Income (USD)", 2000, 20000, 5000)
st.sidebar.markdown("---")

user_profile = {
    "Age": age,
    "Family": family,
    "Risk": risk,
    "Income": income
}

# ---- CHATBOT ----
st.subheader("🤖 Chat with Your Benefits Coach")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "bot", "text": "Hello 👋 I’m your Benefits Coach! Ready to explore the best plans for you?"}
    ]

user_input = st.text_input("You:", placeholder="Type something like 'recommend a plan'...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    if "recommend" in user_input.lower():
        if risk == "Low":
            plan = "Plan A (Low Cost)"
            desc = "Ideal for those who rarely visit doctors. Keeps monthly costs minimal."
        elif risk == "Medium":
            plan = "Plan B (Balanced)"
            desc = "Best for moderate medical needs and balanced cost coverage."
        else:
            plan = "Plan C (Comprehensive)"
            desc = "Top-tier coverage for families or high medical usage."
        response = f"I recommend **{plan}**.\n\n{desc}"
    elif "cost" in user_input.lower():
        response = "Here’s a quick comparison:\n\n- Plan A: $150/month\n- Plan B: $250/month\n- Plan C: $400/month"
    else:
        response = "Try asking me things like: 'Show me plan options' or 'Which is best for a family with kids?'"
    
    st.session_state.chat_history.append({"role": "bot", "text": response})

# Display chat bubbles
for msg in st.session_state.chat_history:
    if msg["role"] == "bot":
        st.markdown(f"<div class='chat-bubble-bot'>💬 <b>Coach:</b> {msg['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-user'>🧑 <b>You:</b> {msg['text']}</div>", unsafe_allow_html=True)

# ---- PLAN SIMULATION ----
st.subheader("📊 Plan Comparison Simulator")

data = pd.DataFrame({
    "Plan": ["Plan A", "Plan B", "Plan C"],
    "Monthly Cost": [150, 250, 400],
    "Coverage Score": [60, 80, 95],
    "Satisfaction (Simulated)": [random.randint(60, 95) for _ in range(3)]
})

st.dataframe(data)
st.bar_chart(data.set_index("Plan")["Monthly Cost"])

# ---- LEARNING CENTER ----
with st.expander("📘 Learn About Each Benefit"):
    st.markdown("""
    **Health Insurance:** Covers doctor visits, hospitalization, and preventive care.  
    **Life Insurance:** Supports your family in case of unforeseen events.  
    **Dental & Vision:** Optional add-ons for extended care.  
    **FSA (Flexible Spending Account):** Tax-advantaged savings for health expenses.
    """)

# ---- SUMMARY SECTION ----
st.subheader("📝 Personalized Summary Sheet (Demo)")

summary = f"""
### Benefits Summary for {family} ({age} years old)
- Risk Tolerance: {risk}
- Monthly Income: ${income}
- Recommended Plan: {plan if 'plan' in locals() else '—'}
"""

st.markdown(summary)
st.download_button("💾 Download Summary (Demo)", summary.encode(), "Benefits_Summary.txt")

st.markdown("---")
st.caption("© 2025 Benefits Choice Coach | Prototype by HR Innovation Lab")
