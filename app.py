from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import json
import os

app = FastAPI()

LOG_CHANNELS_DB = "log_channels.json"

class LogChannel(BaseModel):
    chat_id: str
    channel_id: str

def load_log_channels():
    if os.path.exists(LOG_CHANNELS_DB):
        with open(LOG_CHANNELS_DB, "r") as file:
            return json.load(file)
    return {}

def save_log_channels(log_channels):
    with open(LOG_CHANNELS_DB, "w") as file:
        json.dump(log_channels, file)

@app.post("/setlog")
async def set_log_channel(log_channel: LogChannel):
    log_channels = load_log_channels()
    log_channels[log_channel.chat_id] = log_channel.channel_id
    save_log_channels(log_channels)
    return {"message": "Лог-канал успешно установлен", "log_channel_id": log_channel.channel_id}

@app.get("/getlog/{chat_id}")
async def get_log_channel(chat_id: str):
    log_channels = load_log_channels()
    log_channel_id = log_channels.get(chat_id)
    if not log_channel_id:
        raise HTTPException(status_code=404, detail="Лог-канал не найден")
    return {"channel_id": log_channel_id}
