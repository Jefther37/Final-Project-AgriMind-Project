import streamlit as st
import pandas as pd
import time
from utils.predict import predict_mood
from utils.supabase_client import (
    insert_message,
    fetch_mood_stats,
    register_admin,
    login_admin
)

# Set up page
st.set_page_config(page_title="AgriMind Assistant", layout="wide", page_icon="🌾")
st.markdown(
    """
    <style>
    body {
        background-color: #e8f5e9;
    }
    .stApp {
        background-image: linear-gradient(to bottom right, #e8f5e9, #e3f2fd);
        color: #1b5e20;
    }
    footer {
        font-size: 12px;
        color: #555;
        padding-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.title("🌿 AgriMind: AI-Powered Mental Health Assistant for Farmers")
st.subheader("Monitor mental well-being and visualize community mood")

# --- Authentication ---
st.sidebar.title("Admin Panel")

auth_mode = st.sidebar.radio("Login/Register", ["Login", "Register"])
admin_email = st.sidebar.text_input("Email")
admin_password = st.sidebar.text_input("Password", type="password")

if len(admin_password) < 8:
    st.sidebar.warning("Password must be at least 8 characters.")

auth_success = False
if auth_mode == "Register" and st.sidebar.button("Register"):
    auth_success = register_admin(admin_email, admin_password)
    if auth_success:
        st.sidebar.success("Registered successfully")
    else:
        st.sidebar.error("Registration failed")

elif auth_mode == "Login" and st.sidebar.button("Login"):
    auth_success = login_admin(admin_email, admin_password)
    if auth_success:
        st.sidebar.success("Logged in!")
    else:
        st.sidebar.error("Login failed")

# --- Main App (Only if authenticated) ---
if auth_success:
    tab1, tab2 = st.tabs(["🧠 Mood Analyzer", "📊 Mood Stats"])

    with tab1:
        st.markdown("### Enter your thoughts or feelings")
        user_input = st.text_area("How are you feeling today?", max_chars=300)

        if st.button("Analyze Mood"):
            mood = predict_mood(user_input)
            st.success(f"Detected mood: **{mood.capitalize()}**")

            insert_message(user_input, mood)

            # JS-based Text-to-Speech
            st.markdown(f"""
                <script>
                    var msg = new SpeechSynthesisUtterance("Detected mood is {mood}");
                    window.speechSynthesis.speak(msg);
                </script>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### Mood Trends Dashboard")
        df = fetch_mood_stats()
        if df.empty:
            st.info("No mood data available yet.")
        else:
            # Display table
            st.dataframe(df)

            # Chart
            mood_counts = df['mood'].value_counts()
            st.bar_chart(mood_counts)

            # CSV Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name='mood_stats.csv',
                mime='text/csv'
            )

            # Mood animations
            mood_gif = {
                'positive': "https://media.giphy.com/media/111ebonMs90YLu/giphy.gif",
                'neutral': "https://media.giphy.com/media/xT9IgG50Fb7Mi0prBC/giphy.gif",
                'negative': "https://media.giphy.com/media/26n6WywJyh39n1pBu/giphy.gif"
            }

            if mood in mood_gif:
                st.image(mood_gif[mood], width=200)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px;'>
App developed by <strong>Jefther Afuyo</strong><br>
Contact: <a href='mailto:afuyojefther@gmail.com'>afuyojefther@gmail.com</a>
</div>
""", unsafe_allow_html=True)
