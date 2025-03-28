# Telegram Bot with Gemini AI Integration

A powerful Telegram bot that combines user registration, Gemini AI-powered chat responses, image analysis, and web search capabilities.

## Demo

Watch a demo of the bot in action: [Demo Video](https://drive.google.com/file/d/1y9---xGwfIDoaoxVmETcxIrsp6uCCrcg/view?usp=sharing)

## Features

- 🤖 **AI-Powered Chat**: Powered by Google's Gemini AI for intelligent responses
- 📝 **User Registration**: Collects and stores user information including phone numbers
- 🖼️ **Image Analysis**: Analyzes images and documents using Gemini AI
- 🔍 **Web Search**: Perform web searches with AI-generated summaries
- 💾 **MongoDB Integration**: Persistent storage for user data and chat history

## Prerequisites

- Python 3.7+
- MongoDB running locally or a MongoDB Atlas connection string
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Gemini API Key (from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd telegram-chatbot
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your credentials:
```env
BOT_TOKEN=your_telegram_bot_token
MONGO_URI=your_mongodb_connection_string
GEMINI_API_KEY=your_gemini_api_key
```

## Project Structure

```
telegram-chatbot/
├── main.py              # Main bot application entry point
├── telebot.py           # User registration and contact handling
├── handlers/            # Message and command handlers
│   ├── registration.py  # User registration logic
│   ├── gemini_chat.py   # Gemini AI chat handling
│   ├── image_analysis.py # Image and file analysis
│   └── web_search.py    # Web search functionality
├── requirements.txt     # Project dependencies
└── .env                # Environment variables
```

## Usage

1. Start the bot:
```bash
python main.py
```

2. In Telegram, start a chat with your bot and use the following commands:
- `/start` - Begin user registration
- `/websearch <query>` - Perform a web search
- Send any text message to chat with the AI
- Send images or documents for analysis

## Dependencies

- `python-telegram-bot==20.3` - Telegram Bot API wrapper
- `google-generativeai>=0.3.0` - Google's Gemini AI API
- `python-dotenv>=0.19.0` - Environment variable management
- `motor>=3.1.0` - Async MongoDB driver
- `aiohttp>=3.8.0` - Async HTTP client

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

