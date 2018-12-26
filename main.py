#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
import os
from logzero import logger
from services_grpc.insult_jmk import client as insult_jmk_client
# import find_faces.process_pic as process_pic


TOKEN = os.environ.get('TOKEN')
INSULT_JMK_ADRESS = os.environ.get("INSULT_JMK_HOST", default="localhost") + ":50051"


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    logger.info('Received /start command from %s' % update.message.from_user.username)
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    logger.info('Received /help command from %s' % update.message.from_user.username)
    update.message.reply_text('DANK FACE BOT')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def insult_jmk(bot, update, args=[], groups=("",)):
    """insult jmk"""
    name = groups[0]
    if len(args) > 0:
        name = args[0]

    insult = insult_jmk_client.get_insult(INSULT_JMK_ADRESS, name)
    logger.info("Replied '%s' to '%s'" % (insult, update.message.text))
    update.message.reply_text(insult)


# def dank_face(bot, update):
#     """Send you back your image."""

#     newPhoto = bot.get_file(update.message.photo[-1])
#     fileName = newPhoto.file_id + ".jpg"
#     newPhoto.download(fileName)

#     new_pic = process_pic.run_bot(fileName)
#     logger.info("Find " + str(len(new_pic)) + " faces")

#     try:

#         for i in range(len(new_pic)):
#             try:
#                 bot.send_photo(chat_id=update.message.chat_id, photo=open(new_pic[i], 'rb'))
#             except:
#                 pass
#     except:
#         raise
#     finally:
#         os.remove(fileName)

#         for i in range(len(new_pic)):
#             try:
#                 os.remove(new_pic[i])
#             except:
#                 pass



def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("insult", insult_jmk, pass_args=True))
    dp.add_handler(RegexHandler("(?i)(jmk|jean michel|gaston|jeanmich|jean-mich)", insult_jmk, pass_groups=True))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # dp.add_handler(MessageHandler(Filters.photo, dank_face))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    logger.info("Dank Face Bot is launched !")
    updater.idle()
    logger.info("Dank Face Bot stopped")



if __name__ == '__main__':
    main()