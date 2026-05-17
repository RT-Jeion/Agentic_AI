import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing from your environment setup.")

# Initialize the Bot with modern properties configuration
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Initialize the Master Dispatcher
dp = Dispatcher()

# Initialize a modular router for handling core conversational mechanics
router = Router()

# --- COMMAND ROUTER HANDLER ---
@router.message(Command("start"))
async def handle_start_command(message: types.Message):
    """Listens for the structural /start command."""
    user_name = message.from_user.first_name if message.from_user else "Developer"
    await message.answer(f"👋 Hello {user_name}! Your FastAPI + aiogram Webhook Gateway is running flawlessly.")

# --- RAW TEXT MESSAGE HANDLER ---
@router.message()
async def handle_text_messages(message: types.Message):
    """Listens for any incoming text message that isn't a command."""
    user_text = message.text
    # Ecoing back the message text for testing connection integrity
    await message.answer(f"🤖 Received your message: <i>{user_text}</i>")

# Register the router into the primary master dispatcher
dp.include_router(router)

