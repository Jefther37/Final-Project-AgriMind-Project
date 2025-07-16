import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Load Supabase credentials from Streamlit secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Insert user message and mood into the database
def insert_message(text, mood):
    try:
        response = supabase.table("messages").insert({
            "text": text,
            "mood": mood
        }).execute()
        return response
    except Exception as e:
        st.error(f"Error inserting message: {e}")
        return None

# Fetch historical mood data for visualization and CSV export
def fetch_mood_stats():
    try:
        response = supabase.table("messages").select("*").order("created_at", desc=True).execute()
        data = response.data
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error fetching mood stats: {e}")
        return pd.DataFrame()

# Register an admin (only via email/password)
def register_admin(email, password):
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return True if response.user else False
    except Exception as e:
        st.error(f"Registration failed: {e}")
        return False

# utils/supabase_client.py

def login_admin(email: str, password: str) -> bool:
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response.user is not None
    except Exception as e:
        print("Login error:", e)
        return False
