Steam Game Search Telegram Bot
Description

This Telegram bot allows users to search for games on Steam and get information such as current price, historical low price, and links to the game's Steam page and ProtonDB page. It utilizes the CheapShark API to fetch price data and BeautifulSoup for scraping Steam search results.

Features

    Search for games on Steam.
    Get the current price of the game.
    Obtain the historical lowest price.
    Links to Steam and ProtonDB for further details.

Requirements

    Python 3
    Telegram Bot Token
    Libraries: requests, beautifulsoup4, python-telegram-bot, gazpacho

Setup

    Install the required Python packages:

    pip install -r requirements.txt


Set up a Telegram bot via BotFather on Telegram and get a bot token.

    export BOT_TOKEN='your_telegram_bot_token'

You can also create a .env file and put BOT_TOKEN inside it.

Usage

Run the bot locally with the following command:

    python main.py
Or, if you created the env file:
    
    set -a; source .env; set +a; python main.py   

In Telegram, use the bot's username followed by the game title to initiate a search. For example:

    @YourBotUsername Skyrim

Contributing

Contributions, issues, and feature requests are welcome. Feel free to check issues page if you want to contribute.
License

GPL-3.0 License

Contact

    Original Author: @Alireza6677 - alireza6677@gmail.com
    Updated by: GuaximFsg and jhenrique04 on Github