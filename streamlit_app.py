import streamlit as st
from utils.predict import predict_mood
from utils.supabase_client import insert_message, fetch_mood_stats, register_admin, login_admin
import pandas as pd
import pyttsx3
import time

st.set_page_config(page_title="AgriMind Assistant", layout="wide")

# Initialize TTS engine
engine = pyttsx3.init()

# Custom CSS for theme and layout
st.markdown("""
    <style>
        body {
            background-color: #f0f8f5;
        }
        .main {
            background-color: #e0f2e9;
            border-radius: 10px;
            padding: 20px;
        }
        .footer {
            font-size: 12px;
            color: #666;
            padding-top: 20px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🌿 AgriMind: AI Mental Health Assistant for Farmers")
st.header("Welcome to AgriMind")
st.markdown("Share how you feel and get instant support. Your mental well-being matters.")

# --- User Chat Interaction ---
with st.container():
    st.subheader("🧠 Chat with AgriMind")
    name = st.text_input("Your Name")
    text = st.text_area("How are you feeling today?")
    submit = st.button("Analyze Mood")

    if submit and name and text:
        mood = predict_mood(text)
        insert_message(name, text, mood)

        if mood == "positive":
            response = "That's great to hear! Stay strong and keep going."
            st.success("😊 " + response)
            st.image("https://media.giphy.com/media/26u4lOMA8JKSnL9Uk/giphy.gif", width=300)
        elif mood == "neutral":
            response = "Thanks for sharing. Remember, it’s okay to feel neutral."
            st.info("😐 " + response)
            st.image("https://media.giphy.com/media/l3q2K5jinAlChoCLS/giphy.gif", width=300)
        else:
            response = "I'm here for you. Try to take a break and talk to someone you trust."
            st.error("😔 " + response)
            st.image("https://media.giphy.com/media/f9k1tV7HyORcngKF8v/giphy.gif", width=300)

        engine.say(response)
        engine.runAndWait()

# --- Mood History ---
with st.expander("📊 My Mood History"):
    data = fetch_mood_stats()
    df = pd.DataFrame(data)
    if not df.empty and name:
        user_history = df[df["user_name"] == name]
        st.dataframe(user_history.sort_values("timestamp", ascending=False))
        csv = user_history.to_csv(index=False).encode('utf-8')
        st.download_button("Download My Mood History as CSV", csv, "mood_history.csv", "text/csv")
    else:
        st.write("No mood history available or name not provided.")

# --- Admin Panel ---
st.sidebar.title("🔐 Admin Panel")
auth_action = st.sidebar.radio("Choose Action", ["Login", "Register"])
admin_email = st.sidebar.text_input("Email")
admin_password = st.sidebar.text_input("Password", type="password")
auth_button = st.sidebar.button("Submit")

admin_logged_in = False

if auth_button:
    if auth_action == "Register":
        if len(admin_password) >= 8:
            register_admin(admin_email, admin_password)
            st.sidebar.success("Admin registered successfully!")
        else:
            st.sidebar.error("Password must be at least 8 characters.")
    elif auth_action == "Login":
        if login_admin(admin_email, admin_password):
            admin_logged_in = True
        else:
            st.sidebar.error("Invalid credentials.")

# --- Admin Dashboard ---
if admin_logged_in:
    st.subheader("📈 Admin Dashboard - Mood Analytics")
    data = fetch_mood_stats()
    df = pd.DataFrame(data)

    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        st.write(df.sort_values("timestamp", ascending=False).head())

        st.markdown("### Mood Count Overview")
        st.bar_chart(df["mood"].value_counts())

        st.markdown("### Mood Trends Over Time")
        mood_over_time = df.groupby(df["timestamp"].dt.date)["mood"].value_counts().unstack().fillna(0)
        st.line_chart(mood_over_time)

        csv_admin = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download All Mood Records (Admin)", csv_admin, "all_mood_data.csv", "text/csv")
    else:
        st.warning("No mood records found.")

# --- Footer ---
st.markdown("""
    <hr>
    <div class="footer">
        App developed by Jefther Afuyo | Email: afuyojefther@gmail.com
    </div>
""", unsafe_allow_html=True)
