from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import asyncio

from .db import create_session, log_event
from .llm import stream_llm
from .post_session import summarize_session

router = APIRouter()


@router.websocket("/ws/session/{session_id}")
async def websocket_endpoint(ws: WebSocket, session_id: str):
    await ws.accept()
    create_session(session_id)

    # ---- Conversation State ----
    conversation_mode = "general"

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ]

    try:
        while True:
            user_msg = await ws.receive_text()
            log_event(session_id, "user", user_msg)

            # ---- MULTI-STEP ROUTING LOGIC ----
            if conversation_mode == "general":
                if "summary" in user_msg.lower():
                    conversation_mode = "summary_mode"
                    messages[0]["content"] = (
                        "You are in summarization mode. "
                        "Provide concise and structured responses."
                    )
                elif "help" in user_msg.lower():
                    messages[0]["content"] = (
                        "You are a step-by-step technical assistant."
                    )

            messages.append({"role": "user", "content": user_msg})

            # ---- STREAM RESPONSE ----
            async for token in stream_llm(messages):
                await ws.send_text(token)
                log_event(session_id, "ai", token)

            messages.append({"role": "assistant", "content": ""})

    except WebSocketDisconnect:
        asyncio.create_task(
            asyncio.to_thread(summarize_session, session_id)
        )
