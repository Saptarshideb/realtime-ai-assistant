import asyncio
from .db import fetch_events, save_summary
from .llm import stream_llm


def summarize_session(session_id: str):
    events = fetch_events(session_id)

    if not events:
        save_summary(session_id, "Session ended with no interaction.")
        return

    conversation = []
    for e in events:
        conversation.append(f"{e['event_type']}: {e['content']}")

    summary_prompt = [
        {
            "role": "system",
            "content": "Summarize the following conversation in 3–4 lines."
        },
        {
            "role": "user",
            "content": "\n".join(conversation)
        }
    ]

    async def generate_summary():
        summary_text = ""
        async for token in stream_llm(summary_prompt):
            summary_text += token
        return summary_text

    summary = asyncio.run(generate_summary())
    save_summary(session_id, summary)
