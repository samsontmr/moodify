#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests

from emotion import *

keys = dict([line.split() for line in open('keys')])

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    logger.info("Bot Started")
    logger.info("Keys: %s" % keys)
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def get_input(bot, update):
    if update.message.photo:
        photo_id = update.message.photo[-1].file_id
        json_url = ('https://api.telegram.org/bot' + keys['BotKey'] + 
                    '/getFile?file_id=' + photo_id)
        logger.info(update.message.photo[-1].file_size)
        
        logger.info(requests.get(json_url).json())

        file_path = (requests.get(json_url).json())['result']['file_path']
        photo_url = 'https://api.telegram.org/file/bot' + keys['BotKey'] + "/" + file_path
        logger.info(photo_url)

        photo_file = bot.getFile(update.message.photo[-1].file_id)
        photo_file.download('user_photo.jpg')
        user = update.message.from_user
        
        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = keys['EmotionAPI']
        headers['Content-Type'] = 'application/json' 

        json = { "url": photo_url }
        data = None
        params = None
        
        result = processRequest( json, data, headers, params )
        
        if result is not None:
            # Load the original image, fetched from the URL
            logger.info(result)
            scores = result[0]['scores']
            new_scores = {key: val for key, val in scores.items() if key in ['happiness', 'anger', 'sadness', 'neutral', 'fear']}
            logger.info('Filtered emotions: ' + str(new_scores))
            new_scores = {k: float(v) for k, v in new_scores.items()}
            sorted_scores = [key for (key, value) in sorted(new_scores.items(), key=lambda em:em[1], reverse=True)]
            highest_score = sorted_scores[0]
            
            logger.info(sorted_scores)
            update.message.reply_text(highest_score)
            
            logger.info("Result found")
            

        logger.info("Photo received from %s" % user.first_name)
        update.message.reply_text("Photo received!")
    if update.message.text:
        update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(keys['BotKey'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - get_input the message on Telegram
    dp.add_handler(MessageHandler(Filters.text | Filters.photo, get_input))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
