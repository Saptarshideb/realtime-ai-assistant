import os
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# -----------------------------
# Session lifecycle
# -----------------------------

def create_session(session_id: str, user_id: str = None):
    supabase.table("sessions").insert({
        "session_id": session_id,
        "user_id": user_id
    }).execute()


def log_event(session_id: str, event_type: str, content: str):
    supabase.table("events").insert({
        "session_id": session_id,
        "event_type": event_type,
        "content": content
    }).execute()


def fetch_events(session_id: str):
    result = (
        supabase.table("events")
        .select("*")
        .eq("session_id", session_id)
        .order("timestamp", desc=False)
        .execute()
    )
    return result.data


def save_summary(session_id: str, summary: str):
    # Fetch start_time to calculate duration
    session = (
        supabase.table("sessions")
        .select("start_time")
        .eq("session_id", session_id)
        .single()
        .execute()
    )

    start_time = datetime.fromisoformat(session.data["start_time"])
    end_time = datetime.utcnow()
    duration = int((end_time - start_time).total_seconds())

    supabase.table("sessions").update({
        "summary": summary,
        "end_time": end_time.isoformat(),
        "duration_seconds": duration
    }).eq("session_id", session_id).execute()
