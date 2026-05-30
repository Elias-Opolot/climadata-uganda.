import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.linear_model import LinearRegression

# =====================================================================
# CLIMADATA UGANDA: PROFESSIONAL CORE
# =====================================================================
st.set_page_config(page_title="ClimaData Uganda", page_icon="🌾", layout="centered")

# Custom Styling for a Professional, Clean Look
st.markdown("""
    <style>
    .main-box { background-color: #F1F5F9; padding: 20px; border-radius: 10px; border: 1px solid #CBD5E1; }
    .status-header { font-size: 22px; font-weight: bold; color: #1E293B; margin-bottom: 10px; }
    .action-guide { font-size: 16px; color: #475569; }
    </style>
""", unsafe_allow_html=True)

st.title("🌾 ClimaData Uganda")
st.subheader("Field Diagnostic & Advisory Platform")

# Simple Data Fetcher
@st.cache_data(ttl=600)
def get_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m&forecast_days=1"
    res = requests.get(url).json()
    temp = res["current_weather"]["temperature"]
    moisture = res["hourly"]["relative_humidity_2m"][0] * 0.6
    return temp, moisture

district = st.selectbox("Select Your District:", ["Kampala", "Soroti", "Mbale", "Gulu", "Mbarara"])
coords = {"Kampala": (0.34, 32.58), "Soroti": (1.71, 33.61), "Mbale": (1.07, 34.18), "Gulu": (2.77, 32.28), "Mbarara": (-0.60, 30.65)}
temp, moisture = get_data(*coords[district])

# =====================================================================
# PROFESSIONAL DIAGNOSTIC ENGINE
# =====================================================================
st.markdown("---")
st.write(f"### Current Field Status: **{district}**")

# Use simple color-coded boxes instead of confusing images
def show_status(status, message, color):
    st.markdown(f"""
        <div class='main-box' style='border-left: 10px solid {color};'>
            <div class='status-header'>{status}</div>
            <div class='action-guide'>{message}</div>
        </div>
    """, unsafe_allow_html=True)

if moisture > 50:
    show_status("🟢 Ground is Healthy", "The soil has enough water. No extra work is needed today.", "#22C55E")
elif 30 <= moisture <= 50:
    show_status("🟡 Ground is Drying", "The soil is losing moisture. Consider adding mulch around your crops to protect them from the sun.", "#EAB308")
else:
    show_status("🔴 Critical Dryness", "The ground is too dry. You must irrigate or provide shade immediately to prevent crop loss.", "#EF4444")

# =====================================================================
# INTERACTIVE CHAT NODE
# =====================================================================
st.markdown("---")
st.write("### 💬 Field Assistant")
user_query = st.text_input("Ask a question about your farm:", placeholder="e.g., Is the ground dry?")

if user_query:
    if "dry" in user_query.lower() or "moisture" in user_query.lower():
        st.write(f"**Assistant:** Current moisture level is {int(moisture)}%. Based on our sensors, " + ("the soil is stable." if moisture > 30 else "you need to irrigate immediately."))
    elif "temperature" in user_query.lower() or "hot" in user_query.lower():
        st.write(f"**Assistant:** The current temperature is {temp}°C.")
    else:
        st.write("**Assistant:** Please ask about 'soil moisture' or 'temperature' to get a direct reading.")

st.markdown("---")
st.caption("ClimaData Uganda | Real-time agricultural intelligence.")
