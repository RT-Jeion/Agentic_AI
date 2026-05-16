import os
import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI, Request, BackgroundTasks, status
from fastapi.responses import Response

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# 1. Configuration & Secrets Loading
load_dotenv()  # Required to read the .env file

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g., https://your-codespace-url.github.dev

if not TOKEN or not WEBHOOK_URL:
    raise ValueError("Missing essential environment variables: TELEGRAM_BOT_TOKEN or WEBHOOK_URL")

# 2. Initialize Core Telegram Instances
# In aiogram 3.x+, parse_mode must be passed via DefaultBotProperties
bot = Bot(
    token=TOKEN, 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# 3. Fast Ingestion Background Worker
async def process_agent_rag_pipeline(message_dict: dict):
    """
    This background task is where your slow Agentic RAG system lives.
    Because it runs asynchronously outside the webhook lifecycle, 
    it won't block Telegram's HTTP handshake.
    """
    try:
        # Pydantic v2 native way to rebuild the object safely
        message = types.Message.model_validate(message_dict)
        chat_id = message.chat.id
        user_text = message.text

        print(f"[BACKGROUND WORKER] Processing message from Chat ID {chat_id}: '{user_text}'")

        # --- FUTURE WORKER STEP PLACEHOLDERS ---
        # TODO: Vectorize user_text using sentence-transformers
        # TODO: Query ChromaDB vector database
        # TODO: Pass context to your LangChain Agent loop
        
        # Simulating heavy Agent/LLM processing time (e.g., 3 seconds)
        await asyncio.sleep(3) 
        response_text = f"🤖 Agent response to: <i>{user_text}</i>\n\n(RAG processing mock complete!)"
        
        # Outbound independent POST response back to Telegram API
        await bot.send_message(chat_id=chat_id, text=response_text)
        print(f"[BACKGROUND WORKER] Sent response to Chat ID {chat_id}")

    except Exception as e:
        print(f"[ERROR IN WORKER] Failed to process agent pipeline: {e}")

# 4. Global Application Lifecycle Management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles secure setup and teardown of the Telegram webhook connection."""
    # Action on startup: Tell Telegram where to route updates
    webhook_target = f"{WEBHOOK_URL.rstrip('/')}/webhook"
    print(f"[STARTUP] Setting Telegram webhook destination to: {webhook_target}")
    await bot.set_webhook(url=webhook_target, drop_pending_updates=True)
    
    yield
    
    # Action on shutdown: Clean up connections
    print("[SHUTDOWN] Removing Telegram webhook connection and closing sessions.")
    await bot.delete_webhook()
    await bot.session.close()

# 5. FastAPI App Initialization
app = FastAPI(lifespan=lifespan)

# 6. High-Speed Webhook Endpoint
@app.post("/webhook", status_code=status.HTTP_200_OK)
async def telegram_webhook_router(request: Request, background_tasks: BackgroundTasks):
    """
    Receives incoming payloads from Telegram.
    Validates them, dumps them to a background runner, and exits immediately.
    """
    try:
        # Pull raw JSON update structure from request
        raw_update = await request.json()
        
        # Pydantic v2 native way to validate the incoming dictionary
        update = types.Update.model_validate(raw_update)
        
        # We only care about text messages for this current setup
        if update.message and update.message.text:
            # Drop the raw message dict payload into FastAPI's background thread worker pool
            message_payload = update.message.model_dump()
            background_tasks.add_task(process_agent_rag_pipeline, message_payload)
            
        # Immediately respond 200 OK to Telegram to preserve low latency connection
        return Response(status_code=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"[ERROR IN WEBHOOK] Parsing failure: {e}")
        # Return a 200 regardless to avoid Telegram spamming retries over a malformed payload
        return Response(status_code=status.HTTP_200_OK)

