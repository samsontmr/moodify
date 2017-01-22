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
import os
import requests
import spotify

import emotion_api

#Variables
KEYS = dict([line.split() for line in open('keys')])
WELCOME_MESSAGE = 'Welcome to Moodify!\nSend a selfie to begin'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARN)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    logger.info("Bot Started")
    logger.info("Keys: %s" % KEYS)
    update.message.reply_text(WELCOME_MESSAGE)


def help(bot, update):
    update.message.reply_text('Send a selfie to begin!')

def is_image(url):
    return url.endswith('.jpg') or url.endswith('.jpeg') or url.endswith('.png') or url.endswith('.gif') 

def get_input(bot, update):
    user = update.message.from_user
    if update.message.photo:
        update.message.reply_text("Thinking hard...")
        logger.info("Photo received from %s" % user.first_name)
        photo_id = update.message.photo[-1].file_id
        json_url = ('https://api.telegram.org/bot' + KEYS['BotKey'] + 
                    '/getFile?file_id=' + photo_id)
        logger.info(update.message.photo[-1].file_size)
        
        logger.info(requests.get(json_url).json())

        file_path = (requests.get(json_url).json())['result']['file_path']
        photo_url = 'https://api.telegram.org/file/bot' + KEYS['BotKey'] + "/" + file_path
        logger.info(photo_url)
        
        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = KEYS['EmotionAPI']
        headers['Content-Type'] = 'application/json' 

        json = { "url": photo_url }
        data = None
        params = None
        
        result = emotion_api.processRequest(json, data, headers, params)
        
        if result is not None and result != []:
            # Load the original image, fetched from the URL
            logger.info('Result found: ' + str(result))
            scores = result[0]['scores']
            new_scores = {key: val for key, val in scores.items() 
                          if key in ['happiness', 'anger', 'sadness', 'neutral', 'fear']}
            logger.info('Filtered emotions: ' + str(new_scores))
            new_scores = {k: float(v) for k, v in new_scores.items()}
            sorted_scores = [key for (key, value) in sorted(new_scores.items(), 
                                                            key=lambda em:em[1], reverse=True)]
            highest_score = sorted_scores[0]
            
            logger.info(sorted_scores)
            update.message.reply_text('Enjoy your playlist!\n' + spotify.get_playlist(highest_score))
        else:
           update.message.reply_text("Face not found.\nPlease send a photo with a face") 

    elif not is_image(update.message.text):
        update.message.reply_text("Please send a photo with a face")


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(KEYS['BotKey'])
    PORT = int(os.environ.get('PORT', '5000'))

    updater.start_webhook(listen = "0.0.0.0",
                          port = PORT,
                          url_path = KEYS['BotKey'])
    updater.bot.setWebhook("https://moodify-bot.herokuapp.com/" + KEYS['BotKey'])

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
    #updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
