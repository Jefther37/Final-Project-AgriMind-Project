import streamlit as st
import pandas as pd
from utils.predict import predict_mood
from utils.supabase_client import (
    insert_message, fetch_mood_stats,
    register_admin, login_admin
)
import pyttsx3
import time
from datetime import datetime

# ------------------------ CONFIGURATION ------------------------ #
st.set_page_config(page_title="🌿 AgriMind Assistant", layout="wide")

# ------------------------ HEADER ------------------------ #
st.markdown("""
    <h1 style='color:#228B22;'>🌿 AgriMind: AI-Powered Mental Health Assistant for Farmers</h1>
    <p style='color:#1e90ff;'>Monitor mental well-being and visualize community mood</p>
    <hr style='border-top: 2px solid #ccc;'/>
""", unsafe_allow_html=True)

# ------------------------ CHAT SECTION ------------------------ #
st.subheader("🤖 Talk to AgriMind")

with st.form(key="chat_form"):
    user_name = st.text_input("Your Name")
    user_message = st.text_area("How are you feeling today?")
    submit = st.form_submit_button("Send")

if submit and user_message:
    mood = predict_mood(user_message)
    insert_message(user_name, user_message, mood)

    bot_response = f"I understand you're feeling {mood} today. Take care, {user_name}."
    st.success(f"**Bot:** {bot_response}")

    # Voice (optional)
    try:
        engine = pyttsx3.init()
        engine.say(bot_response)
        engine.runAndWait()
    except:
        st.warning("🔇 Voice feedback is unavailable in cloud deployment.")

# ------------------------ MOOD HISTORY SECTION ------------------------ #
st.subheader("📈 Community Mood Trends")

try:
    df = fetch_mood_stats()
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        mood_count = df['mood'].value_counts()
        st.bar_chart(mood_count)

        # Download CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Mood History CSV", csv, "mood_history.csv", "text/csv")

    else:
        st.info("No mood data yet. Start chatting to populate insights.")

except Exception as e:
    st.error(f"Error loading mood history: {e}")

# ------------------------ ADMIN SECTION ------------------------ #
st.subheader("🔒 Admin Access")

with st.expander("Admin Login / Register"):
    auth_choice = st.radio("Select action", ["Login", "Register"])
    admin_email = st.text_input("Email", key="admin_email")
    admin_password = st.text_input("Password (min 8 characters)", type="password", key="admin_password")

    if st.button("Submit"):
        if auth_choice == "Register":
            success, msg = register_admin(admin_email, admin_password)
        else:
            success, msg = login_admin(admin_email, admin_password)

        if success:
            st.success("✅ Auth successful")
            # Dashboard only visible when logged in
            with st.expander("📊 Admin Dashboard", expanded=True):
                st.write("All mood entries:")
                st.dataframe(df if not df.empty else pd.DataFrame(), use_container_width=True)
        else:
            st.error(f"❌ Auth failed: {msg}")

# ------------------------ FOOTER ------------------------ #
st.markdown("""
    <hr>
    <div style='text-align:center; font-size: 14px; color: #888;'>
        App developed by <strong>Jefther Afuyo</strong><br>
        Contact: afuyojefther@gmail.com
    </div>
""", unsafe_allow_html=True)
