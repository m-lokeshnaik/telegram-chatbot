from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['7546118581:AAETMNsVa4dQ1sTBMPIVDDVN42AEkNijSis']
users_collection = db['users']

def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id

    # Check if user already exists
    if users_collection.find_one({"chat_id": chat_id}):
        update.message.reply_text("You are already registered.")
        return

    # Save user details
    users_collection.insert_one({
        "first_name": user.first_name,
        "username": user.username,
        "chat_id": chat_id
    })

    # Request phone number
    contact_button = KeyboardButton(text="Share your phone number", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True)
    update.message.reply_text("Please share your phone number:", reply_markup=reply_markup)

def contact_handler(update: Update, context: CallbackContext) -> None:
    contact = update.message.contact
    chat_id = update.message.chat_id

    # Update user with phone number
    users_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"phone_number": contact.phone_number}}
    )

    update.message.reply_text("Thank you! Your phone number has been saved.")

def main() -> None:
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.contact, contact_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
