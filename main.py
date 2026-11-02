from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from telethon import TelegramClient

app = FastAPI()

class OtpRequest(BaseModel):
    api_id: int
    api_hash: str
    phone_number: str

@app.post("/send-otp")
async def send_telegram_otp(data: OtpRequest):
    session_name = f"session_{data.phone_number.replace('+', '')}"
    client = TelegramClient(session_name, data.api_id, data.api_hash)
    
    try:
        await client.connect()
        if await client.is_user_authorized():
            await client.disconnect()
            return {"status": "success", "message": "User is already authorized."}
        
        result = await client.send_code_request(data.phone_number)
        await client.disconnect()
        return {
            "status": "success", 
            "message": "OTP code sent successfully!", 
            "phone_code_hash": result.phone_code_hash
        }
    except Exception as e:
        if client.is_connected():
            await client.disconnect()
        raise HTTPException(status_code=400, detail=str(e))
