import streamlit as st
import requests
import pandas as pd

# Set page to wide for a dashboard feel
st.set_page_config(page_title="ClimaData Pro", layout="wide")

# Modern Styling
st.markdown("""
    <style>
    .metric-card { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #e0e0e0; box-shadow: 2px 2px 10px #f0f0f0; }
    .stButton>button { width: 100%; border-radius: 10px; height: 50px; background-color: #2E7D32; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# App Title with a clean header
st.title("🌍 ClimaData Uganda | Intelligence Dashboard")
st.markdown("---")

# Data fetcher
@st.cache_data(ttl=600)
def get_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relative_humidity_2m"
    res = requests.get(url).json()
    return res["current_weather"]["temperature"], res["hourly"]["relative_humidity_2m"][0] * 0.6

# Sidebar Selection
district = st.sidebar.selectbox("📍 Select District Node:", ["Kampala", "Soroti", "Mbale", "Gulu", "Mbarara"])
coords = {"Kampala": (0.34, 32.58), "Soroti": (1.71, 33.61), "Mbale": (1.07, 34.18), "Gulu": (2.77, 32.28), "Mbarara": (-0.60, 30.65)}
temp, moisture = get_data(*coords[district])

# Layout: 3 Columns for metrics
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", f"{temp}°C")
col2.metric("Soil Moisture", f"{int(moisture)}%")
col3.metric("Status", "Stable" if moisture > 30 else "Action Required")

st.markdown("---")

# Chatbot Interface
st.subheader("🤖 Command Center")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Quick Action Buttons
cols = st.columns(3)
if cols[0].button("📊 Get Soil Report"):
    st.session_state.messages.append({"role": "user", "content": "Get Soil Report"})
if cols[1].button("🌡️ Check Temp"):
    st.session_state.messages.append({"role": "user", "content": "Check Temp"})
if cols[2].button("💡 Farming Advice"):
    st.session_state.messages.append({"role": "user", "content": "Farming Advice"})

# Chat Display
for msg in st.session_state.messages:
    with st.chat_message("user"): st.write(msg["content"])
    
    # Generate bot response based on context
    with st.chat_message("assistant"):
        if "Soil" in msg["content"]:
            st.write(f"The soil moisture in {district} is currently at {int(moisture)}%. {'The ground is healthy!' if moisture > 30 else 'We recommend irrigating soon.'}")
        elif "Temp" in msg["content"]:
            st.write(f"The current temperature in {district} is {temp}°C.")
        elif "Farming" in msg["content"]:
            st.write("For this moisture level, we recommend mulching your crops to prevent water evaporation.")
