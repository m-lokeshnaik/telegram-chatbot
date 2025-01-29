import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters  # Use 'filters' instead of 'Filters' for v20+
)
from handlers.registration import start, save_contact
from handlers.gemini_chat import handle_message
from handlers.image_analysis import handle_file
from handlers.web_search import web_search
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    # Initialize application
    app = Application.builder().token(os.getenv("BOT_TOKEN")).build()
    
    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("websearch", web_search))
    
    # Register message handlers
    app.add_handler(MessageHandler(filters.CONTACT, save_contact))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    
    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())