import logging
from datetime import datetime
from typing import Optional

from utils.gemini_api import ask_gemini
from utils.db import get_db
from telegram import Update
from telegram.ext import ContextTypes

# Set up logging
logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles text messages by:
    1. Getting Gemini response
    2. Storing conversation in MongoDB
    3. Sending response to user
    """
    user_message = update.message.text
    chat_id = update.message.chat_id
    response: Optional[str] = None

    try:
        # Get Gemini response
        response = await ask_gemini(user_message)
    except Exception as e:
        logger.error(f"Gemini API error in chat {chat_id}: {str(e)}")
        response = "⚠️ Sorry, I'm having trouble processing your request. Please try again later."

    try:
        # Async MongoDB operations
        db = await get_db()
        await db.chat_history.insert_one({
            "chat_id": chat_id,
            "user_message": user_message,
            "bot_response": response or "Error: No response generated",
            "timestamp": datetime.now(),
            "status": "success" if response else "failed"
        })
    except Exception as e:
        logger.error(f"Database error in chat {chat_id}: {str(e)}")
        response = "⚠️ Message processed, but failed to save history."

    if response:
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("❌ Failed to generate response. Please try again.")