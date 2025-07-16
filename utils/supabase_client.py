import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# Load credentials securely from Streamlit secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Insert a new mood message with timestamp
def insert_message(user_input, mood_label):
    response = supabase.table("messages").insert({
        "message": user_input,
        "mood": mood_label,
        "timestamp": datetime.utcnow().isoformat()
    }).execute()
    return response

# Fetch mood statistics for dashboard
def fetch_mood_stats():
    response = supabase.table("messages").select("mood", "timestamp").execute()
    return response.data

# Admin registration using Supabase Auth
def register_admin(email, password):
    return supabase.auth.sign_up({
        "email": email,
        "password": password
    })

# Admin login using Supabase Auth
def login_admin(email, password):
    return supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })
