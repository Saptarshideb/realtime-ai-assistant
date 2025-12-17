from fastapi import FastAPI
from .websocket_handler import router

app = FastAPI()
app.include_router(router)

@app.get("/")
def root():
    return {"status": "Server running"}
