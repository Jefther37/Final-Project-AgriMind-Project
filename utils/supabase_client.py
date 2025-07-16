from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Insert message into Supabase table
def insert_message(name, message, mood):
    response = supabase.table("messages").insert({
        "user_name": name,
        "message": message,
        "mood": mood
    }).execute()
    return response

# Fetch all mood records
def fetch_mood_stats():
    return supabase.table("messages").select("*").execute().data

# Admin registration
def register_admin(email, password):
    return supabase.auth.sign_up({
        "email": email,
        "password": password
    })

# Admin login
def login_admin(email, password):
    try:
        supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return True
    except Exception:
        return False
