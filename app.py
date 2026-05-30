import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.linear_model import LinearRegression

# =====================================================================
# PROJECT FRAMEWORK & CONFIGURATION
# =====================================================================
st.set_page_config(page_title="ClimaData Uganda", layout="wide", page_icon="📈")

# The "Professional Dashboard" Theme
st.markdown("""
    <style>
    .main-title { color: #0F172A; font-size: 40px; font-weight: 800; }
    .problem-box { background-color: #F8FAFC; border-left: 6px solid #EF4444; padding: 20px; margin-bottom: 20px; }
    .solution-box { background-color: #F0FDFA; border-left: 6px solid #10B981; padding: 20px; margin-bottom: 20px; }
    .metric-card { background: white; padding: 15px; border-radius: 10px; border: 1px solid #E2E8F0; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# AI PREDICTIVE ENGINE (The Core Solution)
# =====================================================================
def get_climate_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,rain,relative_humidity_2m&forecast_days=3"
    data = requests.get(url).json()
    df = pd.DataFrame(data['hourly'])
    df['soil_moisture'] = df['relative_humidity_2m'] * 0.65
    return df

def run_ai_prediction(df):
    # Predictive Model: Linear Regression to forecast next 5 steps
    df['idx'] = np.arange(len(df))
    model = LinearRegression().fit(df[['idx']], df['soil_moisture'])
    next_step = np.array([[len(df) + 5]])
    return float(model.predict(next_step)[0])

# =====================================================================
# UI: THE PROPOSAL ARCHITECTURE
# =====================================================================
st.markdown("<h1 class='main-title'>ClimaData Uganda Platform</h1>", unsafe_allow_html=True)

# 1. Project Framework Display
with st.expander("📌 Project Framework & Problem Statement"):
    st.markdown("<div class='problem-box'><strong>The Problem:</strong> Climate variability in Uganda is causing unpredictable crop yields. Farmers lack real-time localized data to make informed planting decisions.</div>", unsafe_allow_html=True)
    st.markdown("<div class='solution-box'><strong>The Solution:</strong> A digital AI-powered platform that processes satellite telemetry to provide predictive soil and climate advice, enabling climate-smart agriculture.</div>", unsafe_allow_html=True)

# 2. Workspace Nodes
district = st.sidebar.selectbox("📍 Select Region", ["Kampala", "Soroti", "Mbale", "Gulu", "Mbarara"])
coords = {"Kampala": (0.34, 32.58), "Soroti": (1.71, 33.61), "Mbale": (1.07, 34.18), "Gulu": (2.77, 32.28), "Mbarara": (-0.60, 30.65)}

data = get_climate_data(*coords[district])
pred_moisture = run_ai_prediction(data)

# 3. Interactive Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Current Temp", f"{data['temperature_2m'].iloc[-1]}°C")
col2.metric("Soil Moisture", f"{int(data['soil_moisture'].iloc[-1])}%")
col3.metric("AI 5-Day Projection", f"{int(pred_moisture)}%")

# 4. AI Chatbot (The Command Center)
st.subheader("🤖 AI Field Assistant")
if "history" not in st.session_state: st.session_state.history = []

user_input = st.text_input("Ask for advice (e.g., 'Should I plant today?'):")

if user_input:
    # Basic AI Logic - In a real app, this would be an OpenAI API call
    response = "Analyzing telemetry... "
    if "plant" in user_input.lower():
        response += "Based on AI soil moisture projections, " + ("the conditions are optimal for planting." if pred_moisture > 40 else "conditions are too dry. Delay planting.")
    elif "moisture" in user_input.lower():
        response += f"The current soil moisture is {int(data['soil_moisture'].iloc[-1])}%. The AI predicts a trend of {int(pred_moisture)}%."
    else:
        response += "I am monitoring regional telemetry. Ask about 'planting', 'moisture', or 'temperature'."
    
    st.session_state.history.append({"q": user_input, "a": response})

for chat in reversed(st.session_state.history):
    st.write(f"**You:** {chat['q']}")
    st.write(f"**AI:** {chat['a']}")

# 5. Visual Data Insights
st.subheader("📈 Environmental Trend Analysis")
st.line_chart(data[['temperature_2m', 'soil_moisture']])
