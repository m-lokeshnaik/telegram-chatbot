#demo video
https://drive.google.com/file/d/1y9---xGwfIDoaoxVmETcxIrsp6uCCrcg/view?usp=sharing

# Telegram Bot with Gemini AI Integration

## Overview

This project is a Telegram bot that provides user registration, Gemini-powered chat responses, image and file analysis, and web search capabilities. The bot leverages the Gemini API for AI-driven interactions and MongoDB for data storage.

## Features

### User Registration

- Saves user details (first name, username, chat ID) in MongoDB upon first interaction.
- Requests and stores the user's phone number using Telegram's contact button.

### Gemini-Powered Chat

- Uses the Gemini API to generate responses to user queries.
- Stores the full chat history in MongoDB with timestamps.

### Image/File Analysis

- Accepts images and files (e.g., JPG, PNG, PDF) and uses Gemini to describe their content.
- Saves file metadata and analysis results in MongoDB.

### Web Search

- Allows users to perform web searches using the `/websearch` command.
- Returns AI-generated summaries of search results with top web links.

## Installation

### 1. Clone the Repository

```sh
git clone https://github.com/your-repository.git
cd your-repository
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root directory and add the following:

```ini
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
MONGODB_URI=your_mongodb_connection_string
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Run the Bot

```sh
python bot.py
```

## Usage

- **Start the Bot**: Interact with the bot on Telegram by sending the `/start` command.
- **Register**: Share your contact information when prompted to complete registration.
- **Chat**: Send any text message to receive a response from the Gemini API.
- **Analyze Files**: Upload an image or document to receive an analysis.
- **Web Search**: Use the `/websearch` command followed by your query to perform a web search.

## Technologies Used

- **Python**: Programming language for the bot logic.
- **Telegram Bot API**: Interface for interacting with Telegram users.
- **MongoDB**: Database for storing user data and chat history.
- **Gemini API**: AI service for generating chat responses and analyzing content.
- **aiohttp**: Library for making asynchronous HTTP requests.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

