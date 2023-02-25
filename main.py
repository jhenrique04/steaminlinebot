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
import sys
import logging
from uuid import uuid4
from gazpacho import get, Soup
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent



# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text(
        "This bot can search for steam games for you in in-line mode.\n/help for more info.",
    )


def help(update, context):
    update.message.reply_text(
        """To search with this bot you can easily type @Steaminlinebot and then something you want to search. for example :
@Steaminlinebot Skyrim
or
@steaminlinebot Stardew
...""",
    )


def inlinequery(update, context):
    query = update.inline_query.query
    results = []

    prefix = "https://store.steampowered.com/search/?term="
    # "https://wiki.archlinux.org/index.php?profile=default&fulltext=Search&search="

    try:
        page = get(prefix + query)
    except Exception as e:
        update.message.reply_text("Sorry, Steam wiki is offline.")
        logger.error(e)
        return

    html = Soup(page)
    tags = html.find(
        "a", {"data-ds-appid": ""}, mode="all"
    )  # html tags containing info about each game
    pricetags = html.find(
        "div",
        {"class": "col search_price_discount_combined responsive_secondrow"},
        mode="all",
    )
    i = 0
    for tag in tags:
        for pricetag in pricetags:
            price = int(pricetag.attrs["data-price-final"]) * 0.01
            #print(f"Price is {price} and by 100 {price * 100}")
        if i >= 3:
            update.inline_query.answer(results, cache_time=0)
        i = +1
        link = tag.attrs["href"]
        title = tag.text
        appid = tag.attrs["data-ds-appid"]
        #oprint(f"appid is: {appid}")
        #print(f"This is title: {title}\nAnd this is link: {link} and this is appid {appid} and this is PRICE: {price}")
        results.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title=title,
                hide_url=True,
                description=f"Price: {price}",
                thumb_url=f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/capsule_sm_120.jpg?t",  # low qual img
                # description=description,
                input_message_content=InputTextMessageContent(
                    parse_mode="Markdown",
                    message_text=f"[{title}](https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg?)\nPrice:R$ {price:.2f}",
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Steam Page", url=link),
                            InlineKeyboardButton(
                                "ProtonDB page",
                                url=f"https://www.protondb.com/app/{appid}",
                            ),
                            # [InlineKeyboardButton("Protondb")],
                        ]
                    ]
                ),
            )
        )

    update.inline_query.answer(results, cache_time=0)


def error(update, context):
    logger.warning(f"Update {update} caused error {context.error}")


def main():
    # Create the Updater and pass it your bot's token.
    try:
        token = os.environ["BOT_TOKEN"]
    except KeyError:
        logger.critical("No BOT_TOKEN environment variable passed. Terminating.")
        sys.exit(1)
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
