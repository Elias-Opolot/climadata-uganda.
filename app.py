import streamlit as st
import requests

# Layout: Mobile-first design (High contrast, big buttons)
st.set_page_config(page_title="ClimaData Farmer Hub", layout="centered")

st.markdown("""
    <style>
    .big-font { font-size: 24px !important; font-weight: bold; }
    .stButton>button { width: 100%; height: 80px; font-size: 20px; border-radius: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🌾 ClimaData Uganda")
st.write("### What do you want to do today?")

# --- ACTION BUTTONS (The core interaction) ---
col1, col2 = st.columns(2)

if col1.button("🌱 Should I Plant?"):
    st.session_state.action = "PLANT"
if col2.button("💧 Check Soil"):
    st.session_state.action = "SOIL"

# --- SMART FEEDBACK ENGINE ---
if "action" in st.session_state:
    # This logic mimics the AI checking the environment
    # In your real app, this connects to the API/AI model
    if st.session_state.action == "PLANT":
        st.success("🟢 GO AHEAD! The soil has enough moisture for maize.")
    else:
        st.warning("🟡 SOIL IS DRY. Please add mulch (grass/leaves) to keep the roots cool.")
        
    st.write("---")
    st.write("### 🤖 Ask your Assistant:")
    if st.button("🎤 Ask about rain?"):
        st.write("AI Assistant: 'No rain is expected in the next 3 days. Prepare for heat.'")
