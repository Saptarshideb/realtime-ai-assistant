# Realtime AI Assistant



🎯 Goal

Build a real-time conversational backend using WebSockets, LLM interaction, Supabase persistence, and post-session automation.

The system behaves similarly to modern AI chat platforms, where responses are streamed token-by-token and session data is persistently stored and analyzed.

---

Architecture Overview

Client (Browser / Frontend)
        ↓ WebSocket
FastAPI Backend (Async)
        ↓
LLM Streaming Layer (Provider-agnostic)
        ↓
Supabase (PostgreSQL)
        ↓
Post-Session Background Processing

---

Technology Stack

- Backend Framework: FastAPI (async)
- Realtime Communication: WebSockets
- LLM Layer: Provider-agnostic (Mock / Groq / OpenAI supported)
- Database: Supabase (PostgreSQL)
- Async Processing: asyncio
- Frontend: HTML, CSS, JavaScript (WebSocket-based)

---

Project Structure

tecnvirons-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── websocket_handler.py
│   ├── llm.py
│   ├── db.py
│   └── post_session.py
│
├── frontend.html
├── requirements.txt
├── .env
├── .gitignore
└── README.md

---

Environment Variables

Create a `.env` file in the project root:

SUPABASE_URL=https://<your-project>.supabase.co  
SUPABASE_KEY=<your-anon-public-key>

Note: The `.env` file is excluded from version control for security reasons.

---

Supabase Database Schema

Session Metadata Table

create table sessions (
    session_id text primary key,
    user_id text,
    start_time timestamptz default now(),
    end_time timestamptz,
    duration_seconds integer,
    summary text
);

detailed Event Log Table

create table events (
    id bigserial primary key,
    session_id text references sessions(session_id),
    event_type text,
    content text,
    timestamp timestamptz default now()
);

---

Core Requirements Mapping

1. Realtime Session & Streaming

- Framework: FastAPI (asynchronous)
- WebSocket Endpoint: /ws/session/{session_id}
- Streaming: LLM responses are streamed token-by-token to simulate low-latency conversation

2. Complex LLM Interaction

- Multi-step routing based on user intent
- Conversation state management across multiple turns
- Provider-agnostic LLM abstraction

3. Persistence (Supabase)

- Session metadata stored in sessions table
- Granular event logs stored in events table
- All data persisted asynchronously

4. Post-Session Processing

- Triggered on WebSocket disconnect
- Conversation history analyzed by LLM
- Session summary, end time, and duration persisted

---

Running the Application

Install dependencies:

pip install -r requirements.txt

Start server:

uvicorn app.main:app --reload

Server runs at:
http://localhost:8000

---

WebSocket Testing

Endpoint:
ws://localhost:8000/ws/session/{session_id}

Example:
ws://localhost:8000/ws/session/demo123

---

---

Key Design Choices

- WebSockets for real-time communication
- Streaming responses for better UX
- Event-based persistence for auditability
- Async post-processing to avoid blocking sessions
- LLM abstraction for flexibility

---

---

Author: Saptarshi Debnath
