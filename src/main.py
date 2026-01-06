from fastapi import FastAPI, Request, HTTPException, Query
import json
import httpx
from src.services.sales_brain import generate_response
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()

# ==========================================
# 🔑 CRITICAL SETTINGS (Fill these in!)
# ==========================================
VERIFY_TOKEN = "12345"
# Get this from Meta Dashboard > API Setup (Top of page)
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
# Get this from Meta Dashboard > API Setup > Send and receive messages
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
# ==========================================

@app.get("/")
async def health_check():
    return {"status": "alive"}

@app.get("/webhook")
async def verify_webhook(
    mode: str = Query(alias="hub.mode"),
    token: str = Query(alias="hub.verify_token"),
    challenge: str = Query(alias="hub.challenge")
):
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    raise HTTPException(status_code=403, detail="Verification failed")

async def send_reply(to_number: str, text: str):
    """Sends the answer back to WhatsApp"""
    if "YOUR_" in WHATSAPP_TOKEN:
        print("❌ ERROR: You forgot to paste your WHATSAPP_TOKEN in main.py!")
        return

    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "text": {"body": text}
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=data, headers=headers)
        if resp.status_code == 200:
            print("✅ Reply Sent Successfully!")
        else:
            print(f"❌ Failed to send reply: {resp.text}")

@app.post("/webhook")
async def receive_message(request: Request):
    """
    Accepts ANY request to debug why it was failing.
    """
    try:
        # 1. Get the Raw JSON (No strict validation)
        payload = await request.json()
        
        # 2. PRINT IT (So we can see what Meta is sending)
        print("\n📩 RAW PAYLOAD RECEIVED:")
        print(json.dumps(payload, indent=2))

        # 3. Parse it manually
        entry = payload.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        
        if "messages" in value:
            msg = value["messages"][0]
            sender = msg["from"]
            text = msg["text"]["body"]
            
            print(f"👤 User ({sender}): {text}")
            
            # 4. Generate AI Response
            ai_response = await generate_response(text, sender)
            print(f"🤖 AI: {ai_response}")
            
            # 5. Send Reply
            await send_reply(sender, ai_response)
            
        return {"status": "processed"}
        
    except Exception as e:
        print(f"⚠️ Error processing message: {e}")
        return {"status": "error", "detail": str(e)}