import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# Load credentials from Streamlit secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Insert mood message into Supabase
def insert_message(user_input, mood_label):
    response = supabase.table("messages").insert({
