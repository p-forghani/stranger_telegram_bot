import os

import telebot
from loguru import logger
import emoji
from telebot import types

from constants import keyboards
from utils.io import read_json, write_json
from utils.keyboard import create_keyboard


class Bot:
    """Telegram bot to connect 2 strangers to randomly talk
    """
    def __init__(self):
        self.bot = telebot.TeleBot(os.environ['STRANGER_BOT_TOKEN'])
        self.handlers()
        logger.info("Bot starting...")
        self.bot.infinity_polling()

    def handlers(self):
        @self.bot.message_handler(func=lambda _: True)
        def echo_all(message):
            """Send the user the message that recieve

            Args:
                message (_type_): the message that user sends the bot
            """
            write_json(message.json, 'message.json')
            self.bot.send_message(
                message.chat.id,
                message.text,
                reply_markup=keyboards.main
            )

if __name__ == "__main__":
    bot = Bot()
