import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from utils.gemini_api import analyze_file
from utils.db import get_db

# Set up logging
logger = logging.getLogger(__name__)

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles file uploads by:
    1. Downloading the file
    2. Analyzing with Gemini
    3. Storing metadata in MongoDB
    4. Sending analysis to user
    """
    try:
        file = await update.message.document.get_file()
        original_filename = update.message.document.file_name
        file_extension = os.path.splitext(original_filename)[1]
        chat_id = update.message.chat_id

        # Create downloads directory if not exists
        os.makedirs("./downloads", exist_ok=True)
        file_path = f"./downloads/{file.file_id}{file_extension}"
        
        # Download file
        await file.download_to_drive(file_path)
        logger.info(f"Downloaded file: {original_filename} to {file_path}")

        try:
            # Analyze file content
            description = await analyze_file(file_path)
            logger.info(f"Analysis complete for {file.file_id}")
        except Exception as e:
            description = f"⚠️ Analysis failed: {str(e)}"
            logger.error(f"Analysis error: {str(e)}")

        # Store metadata in MongoDB
        try:
            db = await get_db()
            await db.file_analysis.insert_one({
                "chat_id": chat_id,
                "file_id": file.file_id,
                "original_name": original_filename,
                "file_type": update.message.document.mime_type,
                "description": description,
                "timestamp": datetime.now(),
                "status": "success" if "⚠️" not in description else "failed"
            })
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            description += "\n⚠️ Failed to save metadata"

        # Send response
        await update.message.reply_text(
            f"📄 *File Analysis Report*: {original_filename}\n\n"
            f"{description}",
            parse_mode="Markdown"
        )

    except Exception as e:
        logger.error(f"File handling error: {str(e)}")
        await update.message.reply_text("❌ Failed to process file. Please try again.")
    
    finally:
        # Clean up downloaded file
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}")