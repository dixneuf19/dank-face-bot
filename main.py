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
from path import Path

from services_grpc.insult_jmk import client as insult_jmk_client
from services_grpc.find_faces import client as find_faces_client


TOKEN = os.environ.get('TOKEN')
INSULT_JMK_ADDRESS = os.environ.get("INSULT_JMK_HOST", default="localhost") + ":50051"

FIND_FACES_ADDRESS = os.environ.get("FIND_FACES_HOST", default="localhost") + ":50051"
FIND_FACES_PIC_FOLDER = os.environ.get("DOWNLOAD_FOLDER", default="/tmp")



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

    insult = insult_jmk_client.get_insult(INSULT_JMK_ADDRESS, name)
    logger.info("Replied '%s' to '%s'" % (insult, update.message.text))
    update.message.reply_text(insult)


def dank_face(bot, update):
    """Send you back your image."""
    try:
        newPhoto = bot.get_file(update.message.photo[-1])
        fileName = newPhoto.file_id + ".jpg"
        filePath = Path(FIND_FACES_PIC_FOLDER) / Path(fileName)
        newPhoto.download(filePath.abspath())
        logger.info("Picture saved at %s" % filePath)

        result = find_faces_client.find_faces(host=FIND_FACES_ADDRESS, file_path=filePath.abspath())
        logger.info("Found %d faces" % result.nb_faces)
        
        for i in range(len(result.faces)):
            try:
                update.message.reply_photo(photo=open(result.faces[i].path, 'rb'))
            except Exception as error:
                logger.warn("Failed to send face %d : %s" % (i, error))

    except Exception as error:
        logger.error("Error in dank_face: %s" % error)
    


    # try:

    #     
    # except:
    #     raise
    # finally:
    #     os.remove(fileName)

    #     for i in range(len(new_pic)):
    #         try:
    #             os.remove(new_pic[i])
    #         except:
    #             pass



def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.info("Entered in error function")
    logger.warn('Update "%s" caused error "%s"', update, error)

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

    dp.add_handler(MessageHandler(Filters.photo, dank_face))

    dp.add_handler(RegexHandler("(?i)(jmk|jean michel|gaston|jeanmich|jean-mich)", insult_jmk, pass_groups=True))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))
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