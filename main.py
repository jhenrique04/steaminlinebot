#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Telegram bot for searching through Steam and protondb pages
# This program is dedicated to the public domain under the GPL3 license.

"""
Original archewiki bot Written by: @Alireza6677
                                   alireza6677@gmail.com

original archewikibot Updated in 27/05/2021 by: @NicKoehler
"""
"""
@Steaminlinebot written by GuaximFsg on github
"""

import os
import logging
import requests
import sys
from uuid import uuid4
from bs4 import BeautifulSoup
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext

MAXRESULTS = 4

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("This bot can search for steam games for you in in-line mode.\n/help for more info.")


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("To search with this bot you can easily type @Steaminlinebot and then something you want to search. for example:\n@SteamInlineSearchBot Skyrim")


def get_game_price(game_title: str):
    url = f"https://www.cheapshark.com/api/1.0/games?title={game_title}&limit=1"
    response = requests.get(url)
    games = response.json()

    if not games:
        return "No price data available", None, None

    game = games[0]
    price_info = f"Price: ${game['cheapest']}"
    thumb_url = game.get('thumb', '')
    deal_id = game['cheapestDealID']

    history_url = f"https://www.cheapshark.com/api/1.0/deals?id={deal_id}"
    history_response = requests.get(history_url)
    history_data = history_response.json()

    historic_low = history_data.get('gameInfo', {}).get('salePrice', "No historical data")

    return price_info, historic_low, thumb_url


def inlinequery(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    results = []

    prefix = "https://store.steampowered.com/search/?term="
    try:
        response = requests.get(prefix + query)
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        logger.error(e)
        return

    tags = soup.find_all("a", attrs={"data-ds-appid": True}, limit=MAXRESULTS)
    
    for tag in tags:
        appid = tag['data-ds-appid']
        title = tag.find("span", class_="title").text if tag.find("span", class_="title") else "No Title"
        price_info, historic_low, thumb_url = get_game_price(title)
        link = tag['href']
        
        buttons = [
            InlineKeyboardButton("Steam 💨", url=link),
            InlineKeyboardButton("ProtonDB 🐧", url=f"https://www.protondb.com/app/{appid}")
        ]

        results.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title=title,
                hide_url=True,
                description=price_info,
                thumb_url=thumb_url,
                input_message_content=InputTextMessageContent(
                    message_text = f"[{title}]({link})\n{price_info}\nHistoric Low: ${historic_low}",
                    parse_mode="Markdown"
                ),
                reply_markup=InlineKeyboardMarkup([buttons]),
            )
        )

    update.inline_query.answer(results, cache_time=0)


def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f"Update {update} caused error {context.error}")


def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        logger.critical("No BOT_TOKEN environment variable found. Terminating.")
        sys.exit(1)

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()