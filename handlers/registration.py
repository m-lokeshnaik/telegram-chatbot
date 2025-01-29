# handlers/registration.py (async version)
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utils.db import get_db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.message.from_user
        chat_id = update.message.chat_id
        
        db = await get_db()
        existing_user = await db.users.find_one({"chat_id": chat_id})

        if not existing_user:
            await db.users.insert_one({
                "chat_id": chat_id,
                "first_name": user.first_name,
                "username": user.username,
                "registered_at": datetime.now(),
                "status": "pending"
            })
            contact_keyboard = ReplyKeyboardMarkup(
                [[KeyboardButton("📱 Share Phone Number", request_contact=True)]],
                resize_keyboard=True,
                one_time_keyboard=True
            )
            await update.message.reply_text(
                "Welcome! Please share your phone number.",
                reply_markup=contact_keyboard
            )
        else:
            await update.message.reply_text("You're already registered!")

    except Exception as e:
        logger.error(f"Start error: {str(e)}")
        await update.message.reply_text("⚠️ Registration failed. Please try again.")

async def save_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        contact = update.message.contact
        chat_id = update.message.chat_id
        
        db = await get_db()
        result = await db.users.update_one(
            {"chat_id": chat_id},
            {"$set": {
                "phone_number": contact.phone_number,
                "status": "verified",
                "verified_at": datetime.now()
            }}
        )
        
        if result.modified_count == 1:
            await update.message.reply_text("✅ Registration complete!")
        else:
            await update.message.reply_text("⚠️ Failed to save contact")

    except Exception as e:
        logger.error(f"Contact error: {str(e)}")
        await update.message.reply_text("⚠️ Contact save failed")