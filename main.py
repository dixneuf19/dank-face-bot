#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Application class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import asyncio
import os
import time
from random import randint

import requests
from dotenv import load_dotenv
from loguru import logger
from path import Path
from requests.exceptions import HTTPError
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
INSULT_JMK_ADDRESS = f'{os.getenv("INSULT_JMK_HOST", default="localhost")}:{os.getenv("INSULT_JMK_PORT", default="80")}'
FUZZY_OCTO_DISCO_ADDRESS = f'{os.getenv("FUZZY_OCTO_DISCO_HOST", default="http://localhost")}:{os.getenv("FUZZY_OCTO_DISCO_PORT", default="80")}'

FIND_FACES_PIC_FOLDER = os.getenv("DOWNLOAD_FOLDER", default="/tmp/pics")
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", default="20"))
HONK_FILE_ID = os.getenv(
    "HONK_FILE_ID",
    "CQACAgQAAxkBAAICGmHI3e4vqCQLZctOeQsR7iStMr0VAAL9CQACZUZJUr9MlakXmVAzIwQ",
)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    logger.info("Received /start command from %s" % update.message.from_user.username)
    await update.message.reply_text("Hi!")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    logger.info("Received /help command from %s" % update.message.from_user.username)
    await update.message.reply_text("DANK FACE BOT")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


# def insult_jmk(update: Update, context: ContextTypes.DEFAULT_TYPE, args=[], groups=("",)):
#     """insult jmk"""
#     logger.info(
#         f"Received an insult request from '{update.message.from_user.name}' in chat '{update.message.chat.title}'"
#     )

#     name = groups[0]
#     if len(args) > 0:
#         name = args[0]

#     logger.info("Received /insult command from %s" % update.message.from_user.username)

#     insult = insult_jmk_client.get_insult(INSULT_JMK_ADDRESS, name)
#     logger.info("Replied '%s' to '%s'" % (insult, update.message.text))
#     update.message.reply_text(insult)


async def bonne_annee(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from_user = update.message.from_user.first_name
    await update.message.reply_text(
        "🎉🎉🎉\nBonne année %s !\n🥂🥂🥂\nDoot doot spam !\n🎊🎊🎊" % from_user
    )


async def honk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        f"Received an honk request from '{update.message.from_user.name}' in chat '{update.message.chat.title}'"
    )
    await update.message.reply_audio(
        audio=HONK_FILE_ID,
        caption="HONK! HONK! HONK!",
    )


async def dank_face(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send you back your image."""
    logger.info(
        f"Received a image from '{update.message.from_user.name}' in chat '{update.message.chat.title}'"
    )
    try:
        newPhoto = await update.message.photo[-1].get_file()
        fileName = newPhoto.file_id + ".jpg"
        filePath = Path(FIND_FACES_PIC_FOLDER) / Path(fileName)
        await newPhoto.download_to_drive(filePath.abspath())
        logger.info("Picture saved at %s" % filePath)

        try:
            res = await asyncio.to_thread(
                requests.get,
                f"{FUZZY_OCTO_DISCO_ADDRESS}/faces",
                params={"pic_path": filePath},
            )
            res.raise_for_status()
            result = res.json()
            if result["status"] == "SUCCESS":
                logger.info("Found %d faces" % result["nbFaces"])
                for i in range(int(result["nbFaces"])):
                    try:
                        # TODO: send as an album https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html?highlight=album#telegram.Bot.send_media_group
                        await update.message.reply_photo(
                            photo=open(result["paths"][i], "rb"),
                            read_timeout=DEFAULT_TIMEOUT,
                            write_timeout=DEFAULT_TIMEOUT,
                        )
                    except Exception as error:
                        logger.warning("Failed to send face %d : %s" % (i, error))
                        pass
                    finally:
                        try:
                            # Remove the file
                            Path(result["paths"][i]).remove_p()
                        except Exception as error:
                            logger.debug("Failed to remove face %d : %s" % (i, error))
                            pass

            elif result["status"] in ("NO_FACE_FOUND", "FAILED_ALL_FACES"):
                dog_number = randint(1, 43)
                await update.message.reply_photo(
                    photo=open(f"./amazon_dogs/{dog_number}.-TTD-c.jpg", "rb"),
                    caption="Sorry, didn't find any faces 😢",
                    read_timeout=DEFAULT_TIMEOUT,
                    write_timeout=DEFAULT_TIMEOUT,
                )
            else:
                logger.warning(
                    f"Received {result['status']} from fuzzy-octo-disco: {result['message']}"
                )
        except HTTPError as e:
            logger.error(e)
            raise e
        finally:
            filePath.remove_p()

    except Exception as error:
        logger.error("Error in dank_face: %s" % error)
        if "Not enough rights to send photos to the chat" in str(error):
            await update.message.reply_text("Give me right to send photos or kick me!")
        else:
            raise error


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    logger.info("Entered in error function")
    logger.warning(f"Update {update} caused error {context.error}")


def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    # The library defaults to 5 s, too short for get_file on forwarded photos
    dp = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .connect_timeout(DEFAULT_TIMEOUT)
        .read_timeout(DEFAULT_TIMEOUT)
        .write_timeout(DEFAULT_TIMEOUT)
        .media_write_timeout(DEFAULT_TIMEOUT)
        .build()
    )

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # dp.add_handler(CommandHandler("insult", insult_jmk, pass_args=True))
    dp.add_handler(CommandHandler("honk", honk))

    dp.add_handler(MessageHandler(filters.PHOTO, dank_face))

    # dp.add_handler(RegexHandler("(?i)(jmk|jean michel|gaston|jeanmich|jean-mich)", insult_jmk, pass_groups=True))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(filters.TEXT, bonne_annee))
    # log all errors
    dp.add_error_handler(error_handler)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT.
    logger.info("Dank Face Bot is launched !")
    dp.run_polling()
    logger.info("Dank Face Bot stopped")


if __name__ == "__main__":
    main()
