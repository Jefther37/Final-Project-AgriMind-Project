import streamlit as st
import pandas as pd
import time
from utils.predict import predict_mood
from utils.supabase_client import (
    insert_message, fetch_mood_stats,
    register_admin, login_admin
)
import streamlit.components.v1 as components

st.set_page_config(page_title="AgriMind Assistant", layout="wide")

# 🌿 Title and Info
st.title("🌿 AgriMind: AI-Powered Mental Health Assistant for Farmers")
st.markdown("Monitor mental well-being and visualize community mood")
st.markdown("**App developed by Jefther Afuyo**  \nContact: afuyojefther@gmail.com")

# 🔊 Function for Web Text-to-Speech
def speak(message):
    components.html(
        f"""
        <script>
        var msg = new SpeechSynthesisUtterance();
        msg.text = `{message}`;
        window.speechSynthesis.speak(msg);
        </script>
        """,
        height=0,
    )

# Sidebar navigation
menu = st.sidebar.radio("Navigation", ["🤖 Chatbot", "📈 Mood History", "🛡 Admin Login / Register"])

# SESSION state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 💬 Chatbot Page
if menu == "🤖 Chatbot":
    name = st.text_input("Enter your name:")
    user_message = st.text_input("Send a message:")

    if st.button("Send"):
        if name and user_message:
            prediction = predict_mood(user_message)
            insert_message(name, user_message, prediction)
            st.session_state.messages.append((name, user_message, prediction))
            st.success(f"🧠 Mood Prediction: {prediction}")
            speak(f"Your mood seems to be {prediction}")
        else:
            st.warning("Please enter your name and a message.")

    st.markdown("### 💬 Chat History")
    for msg in st.session_state.messages[::-1]:
        st.info(f"{msg[0]}: {msg[1]} → 🧠 Mood: {msg[2]}")

# 📊 Mood History Page
elif menu == "📈 Mood History":
    df = fetch_mood_stats()
    if df is not None and not df.empty:
        st.markdown("### 📊 Community Mood Overview")
        st.dataframe(df)
        mood_counts = df['mood'].value_counts()
        st.bar_chart(mood_counts)
    else:
        st.warning("No mood data available yet.")

# 🔐 Admin Page
elif menu == "🛡 Admin Login / Register":
    st.markdown("### 👤 Admin Authentication")

    auth_option = st.radio("Choose action", ["Register", "Login"])

    admin_email = st.text_input("Email")
    admin_password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if auth_option == "Register":
            try:
                register_admin(admin_email, admin_password)
                st.success("✅ Admin registered successfully!")
            except Exception as e:
                st.error(f"Registration failed: {e}")
        else:
            try:
                user = login_admin(admin_email, admin_password)
                st.success("✅ Logged in successfully!")
                st.json(user)
            except Exception as e:
                st.error(f"Login failed: {e}")

# 🌍 Footer Section
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: 14px; color: grey;'>
        &copy; 2025 AgriMind | Developed by <strong>Jefther Simeon Afuyo</strong> |
        Contact: <a href="mailto:afuyojefther@gmail.com">afuyojefther@gmail.com</a>
    </div>
    """,
    unsafe_allow_html=True
)
# Add a small delay to ensure the page loads smoothly