import os
from supabase import create_client, Client
from datetime import datetime
import pandas as pd
import streamlit as st

# Load Supabase credentials from Streamlit secrets
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------ Insert Chat Message ------------------ #
def insert_message(name: str, message: str, mood: str):
    try:
        response = supabase.table("messages").insert({
            "name": name,
            "message": message,
            "mood": mood,
            "timestamp": datetime.now().isoformat()
        }).execute()
        return True, "Message saved"
    except Exception as e:
        return False, f"Insert failed: {e}"

# ------------------ Fetch Mood Stats ------------------ #
def fetch_mood_stats():
    try:
        response = supabase.table("messages").select("*").order("timestamp", desc=True).execute()
        records = response.data
        if records:
            df = pd.DataFrame(records)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        print("Error fetching mood stats:", e)
        return pd.DataFrame()

# ------------------ Register Admin ------------------ #
def register_admin(email: str, password: str):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    try:
        auth_response = supabase.auth.sign_up({"email": email, "password": password})
        if auth_response.user:
            return True, "Registration successful"
        else:
            return False, "Registration failed"
    except Exception as e:
        return False, str(e)

# ------------------ Login Admin ------------------ #
def login_admin(email: str, password: str):
    try:
        auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if auth_response.user:
            return True, "Login successful"
        else:
            return False, "Login failed"
    except Exception as e:
        return False, str(e)
