#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import telegram
import numpy as np
from PIL import Image
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tensorflow import keras
from tensorflow.keras.preprocessing import image as image_keras
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
model = keras.models.load_model('./basic.h5')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def about(update, context):
    update.message.reply_text('https://tinyurl.com/bdd57jxp')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    # print(update.message)
    # print(update.message.photo)
    update.message.reply_text("Please upload image")

id = 0 
def invert(update, context):
    """Echo the user message."""
    global id
    new_file = update.message.photo[-1].get_file()
    filename = 'downloads/file{}.jpg'.format(id)
    new_file.download(filename)
    image = Image.open(filename)

    if is_tree(filename):
        rotated_image = image.rotate(180)
        rotated_image.save(filename)
        id += 1
        reply_is_tree(update, filename)
    else:
        reply_not_tree(update)

def reply_is_tree(update, filename):
    update.message.reply_text("Hey! Looks like your tree is upside down. Here's the tree again in the "
    + "correct orientation.")
    update.message.reply_photo(open(filename, 'rb'))

def reply_not_tree(update):
    update.message.reply_photo(open('./default_reply.jpg', 'rb'))

def is_tree(image_file_path):
    image = image_keras.load_img(image_file_path, target_size=(299, 299))
    image_array = image_keras.img_to_array(image)
    image_batch = np.expand_dims(image_array, axis=0)
    image_preprocessed = preprocess_input(image_batch)
    return model.predict(image_preprocessed)[0][0] == 1

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("5012350483:AAH1JhRaPcYz39uALFGcXI8jfGp8Jmv5L-w", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("about", about))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.photo, invert))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
