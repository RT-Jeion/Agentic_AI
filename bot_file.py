import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

from dotenv import load_dotenv
load_dotenv()
# Replace this with your actual Bot Token from @BotFather
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Setup logging to monitor progress in the Codespaces terminal
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback function triggered whenever a file/document is received."""
    # Ensure there is a message and a document in the update
    if not update.message or not update.message.document:
        return

    document = update.message.document
    file_name = document.file_name or f"file_{document.file_id[:8]}"
    new_file = f"memory/{file_name}"
    print(f"\n📥 Detecting incoming file: {file_name}")
    
    try:
        # 1. Correctly fetch the File object using the bot instance
        tg_file = await context.bot.get_file(document.file_id)
        
        # 2. Define the absolute destination path inside your Codespace
        custom_path = os.path.join(os.getcwd(), new_file)
        
        print(f"⏳ Downloading and saving directly to Codespaces...")
        
        # 3. Call the modern async download method on the file object
        await tg_file.download_to_drive(custom_path)
        
        print(f"✅ Successfully saved to: {custom_path}\n")
        await update.message.reply_text(f"Successfully saved {file_name} to Codespaces!")
        
    except Exception as e:
        print(f"❌ Error handling file: {e}")
        if update.message:
            await update.message.reply_text(f"Failed to download file. Error: {e}")

def main():
    """Start the bot listener."""
    # Build the application wrapper
    application = Application.builder().token(BOT_TOKEN).build()

    # Register the handler specifically looking for any Document type file
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("🚀 Bot listener is running safely... Send your file from Termux!")
    
    # Run the polling thread (blocks until Ctrl+C is pressed)
    application.run_polling(allowed_updates=Update.ALL)

if __name__ == "__main__":
    main()

