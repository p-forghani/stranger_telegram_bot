import os

import emoji
import telebot
from loguru import logger
from telebot import types

from constants import keyboards
from utils.custom_filters import IsPouria
from utils.io import read_json, write_json
from utils.keyboard import create_keyboard


class Bot:
    """Telegram bot to connect 2 strangers to randomly talk
    """
    def __init__(self, bot_token):
        # Build the bot
        self.bot = telebot.TeleBot(bot_token)
        # Add the logic to the bot
        self.handlers()
        # Register the custom filters
        self.bot.add_custom_filter(IsPouria())
        logger.info("Bot starting...")
        # Run the bot
        self.bot.infinity_polling()

    def handlers(self):
        @self.bot.message_handler(func=lambda _: True)
        def echo_all(message: telebot.types.Message):
            """Send the user the message that recieve

            Args:
                message (_type_): the message that user sends the bot
            """
            write_json(message.json, "data/message.json")
            self.bot.send_message(
                message.chat.id,
                message.text,
                reply_markup=keyboards.main
            )

        @self.bot.message_handler(is_pouria=True)
        def hi_pouria(message: telebot.types.Message):
            """Say hi to Pouria

            Args:
                message (telebot.types.Message): _description_
            """
            self.bot.reply_to(message, 'Hi Pouria')
