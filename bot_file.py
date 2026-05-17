import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

from dotenv import load_dotenv
load_dotenv()

# Replace this with your actual Bot Token from @BotFather
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Enable basic logging to see what's happening in the terminal
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback function triggered whenever a file/document is received."""
    document = update.message.document
    file_name = document.file_name
    
    print(f"📥 Detecting incoming file: {file_name}")
    
    # Get the file object from Telegram's servers
    tg_file = await context.bot.get_file(document.file_id)
    
    # Define where to save it (current working directory)
    custom_path = os.path.join(os.getcwd(), file_name)
    
    print(f"⏳ Downloading {file_name}...")
    # Download and save the file locally
    await tg_file.download_to_drive(custom_path)
    
    print(f"✅ Successfully saved to: {custom_path}\n")
    await update.message.reply_text(f"Successfully saved {file_name} to Codespaces!")

def main():
    """Start the bot listener."""
    # Create the application configuration
    application = Application.builder().token(BOT_TOKEN).build()

    # Register a handler that listens specifically for documents/files
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("🚀 Bot listener is running... Send a file from Termux or Telegram app.")
    
    # Run the bot until you press Ctrl+C in the terminal
    application.run_polling(allowed_updates=Update.ALL)

if __name__ == "__main__":
    main()

