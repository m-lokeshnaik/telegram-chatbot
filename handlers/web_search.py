from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import logging
from datetime import datetime
from utils.db import get_db
from utils.web_scraper import perform_web_search

# Set up logging
logger = logging.getLogger(__name__)

async def web_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /websearch command:
    1. Validates search query
    2. Performs web search
    3. Stores search history
    4. Presents formatted results
    """
    try:
        # Validate query
        query = " ".join(context.args).strip() if context.args else ""
        if not query or len(query) > 200:
            await update.message.reply_text(
                "🔍 Please provide a valid search query (1-200 characters)\n"
                "Example: /websearch AI trends 2024"
            )
            return

        # Show typing indicator
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, 
            action="typing"
        )

        # Perform search
        try:
            search_results = await perform_web_search(query)
            summary, links = search_results if search_results else ("No results found", [])
        except Exception as e:
            logger.error(f"Search error for '{query}': {str(e)}")
            await update.message.reply_text("⚠️ Search service unavailable. Please try again later.")
            return

        # Format response
        response = (
            f"📚 *Search Results for* '{query}':\n\n"
            f"{summary}\n\n"
            "🔗 *Top Resources*:\n"
        )
        
        # Build links list with Markdown formatting
        formatted_links = []
        for idx, (title, url) in enumerate(links[:5], 1):
            formatted_links.append(f"{idx}. [{title}]({url})")
        
        full_response = response + "\n".join(formatted_links) if formatted_links else response + "No links available"

        # Store search history
        try:
            db = await get_db()
            await db.search_history.insert_one({
                "chat_id": update.message.chat_id,
                "query": query,
                "result_count": len(links),
                "timestamp": datetime.now(),
                "status": "success" if links else "no_results"
            })
        except Exception as e:
            logger.error(f"Search history save error: {str(e)}")

        # Send response with pagination buttons
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refine Search", switch_inline_query_current_chat=query)]
        ])

        await update.message.reply_text(
            text=full_response,
            parse_mode="Markdown",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

    except Exception as e:
        logger.error(f"Web search handler error: {str(e)}")
        await update.message.reply_text("❌ Failed to process your search request. Please try again later.")