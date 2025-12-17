from groq import Groq
import asyncio

client = Groq()

async def stream_llm(messages):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        stream=True
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            await asyncio.sleep(0)  # keep async flow
            yield chunk.choices[0].delta.content
