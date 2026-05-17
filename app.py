import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI, Request, status
from fastapi.responses import Response
from aiogram import types

# Import our initialized bot and master dispatcher instances
from bot import bot, dp

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
SECRET_PATH = os.getenv("WEBHOOK_SECRET_PATH", "tg-webhook-gateway")

if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL is missing from your environment setup.")

# --- LIFECYCLE MANAGEMENT ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles the synchronization of the webhook target on boot and teardown."""
    # Build target string (e.g., https://yourdomain.com/tg-webhook-gateway)
    webhook_target = f"{WEBHOOK_URL.rstrip('/')}/{SECRET_PATH}"
    print(f"[STARTUP] Syncing webhook route targets with Telegram: {webhook_target}")
    
    # Send configuration registration payload to Telegram
    await bot.set_webhook(url=webhook_target, drop_pending_updates=True)
    
    yield
    
    # Clean up hooks cleanly upon process termination signals
    print("[SHUTDOWN] Severing active webhook registries and dropping active client sessions.")
    await bot.delete_webhook()
    await bot.session.close()

# Initialize our Web Server instance
app = FastAPI(lifespan=lifespan)

# --- SECURED WEBHOOK ROUTER ENDPOINT ---
@app.post(f"/{SECRET_PATH}", status_code=status.HTTP_200_OK)
async def process_incoming_telegram_updates(request: Request):
    """
    Acts as the ingestion gate. Validates the structure, feeds it to the
    aiogram pipeline, and issues a 200 OK verification code back to Telegram.
    """
    try:
        # Extract raw JSON network payload
        raw_update = await request.json()
        
        # Strictly validate array maps against aiogram's core Update scheme models
        update = types.Update.model_validate(raw_update, context={"bot": bot})
        
        # Feed the update straight into the dispatcher's asynchronous handler loop
        # This triggers command structures like /start naturally inside bot.py
        await dp.feed_update(bot=bot, update=update)
        
        return Response(status_code=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"[GATEWAY ERROR] Exception caught processing frame: {e}")
        # Always return a 200 back to Telegram to avoid automated payload delivery retries
        return Response(status_code=status.HTTP_200_OK)

