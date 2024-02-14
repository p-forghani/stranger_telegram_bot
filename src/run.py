<<<<<<< HEAD
import telebot
from loguru import logger
from src.bot import BOT
import emoji
import time

from src.constants import keyboards, keys, states
from src.db import db
import pymongo

class Bot:
    """Telegram bot to connect 2 strangers to randomly talk
    """
    def __init__(self, telebot: telebot.TeleBot, db: pymongo.MongoClient):
        # Build the bot
        self.bot = telebot
        self.db = db

        # Register the handlers
        self.handlers()

    def run(self):
        logger.info("Bot starting...")
        self.bot.infinity_polling()

    def handlers(self):

        # TODO: Stop the user if it is a bot

        # Go to the main menu
        @self.bot.message_handler(func=lambda message: message.text in [
            '/start', emoji.emojize(keys.exit)
        ])
        def start(message: telebot.types.Message):
            # Send initial message to user
            self.send_message(
                message.from_user.id,
                f'Hi {message.from_user.first_name}, welcome to the Stranger bot!',
                reply_markup=keyboards.main
            )
            # Update user info in db
            self.db.users.update_one(
                {'user_id': message.from_user.id},
                {'$set': message.json['from']},
                upsert=True
            )
            # Update user state to main
            self.update_state(message.from_user.id, states.main)
            logger.info("User's state updated to MAIN")
            logger.info(f'User {message.from_user.id} Started the bot')

        @self.bot.message_handler(regexp=emoji.emojize(keys.random_connect))
        def random_connect(message):

            # Change state of the user
            self.update_state(message.from_user.id, states.online)
            logger.info(f'User {message.from_user.id} state updated to ONLINE')
            user_id = message.from_user.id

            # Send proper message to user
            self.send_message(
                user_id,
                'Connecting you to a stranger...',
                reply_markup=keyboards.exit
            )
            logger.info('Message Sent to User')

            # find the other online <user_id>
            other_user = self.db.users.find_one(
                {
                    'state': states.online,
                    'user_id': {'$ne': user_id}
                }
            )

            if not other_user:
                return
            logger.info(f"other_user = \n{other_user}")


            # Update user state
            self.update_state(user_id, states.connected)
            # Update other user state
            self.update_state(other_user['user_id'], states.connected)

            # Update `connected_to` field of user
            self.db.users.update_one(
                {'user_id': user_id},
                {'$set': {'connected_to': other_user['user_id']}},
                upsert=True
            )
            # Update `connected_to` field of the other user
            self.db.users.update_one(
                {'user_id': other_user['user_id']},
                {'$set': {'connected_to': user_id}},
                upsert=True
            )

            # Send proper message to both users
            self.send_message(
                user_id,
                f"You are connected to user {other_user['user_id']}"
            )
            self.send_message(
                other_user['user_id'],
                f'You are connected to user {user_id}'
            )

        # TODO: Implement the exit command

        @self.bot.message_handler(func=lambda _: True)
        def echo(message: telebot.types.Message):
            """Echo message to the other connected user

            Args:
                message (telebot.types.Message): _description_
            """
            logger.info(f'{message.text} Recieved')
            user = self.db.users.find_one(
                {'user_id': message.from_user.id}
            )
            if (
                (not user) or
                (user['state'] != states.connected) or
                (user['connected_to'] is None)
            ):
                logger.info('Bot Returned None')
                return
            self.send_message(
                user['connected_to'],
                message.text
            )
            logger.info(f"{message.text} Sent to User {user['connected_to']}")

    def send_message(self, chat_id, text, reply_markup=keyboards.exit):
        self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

    def update_state(self, user_id, state):
        self.db.users.update_one(
            {'user_id': user_id},
            {"$set": {
                'state': state
            }},
            upsert=True
        )

if __name__ == '__main__':
    stranger_bot = Bot(BOT, db)
    stranger_bot.run()
=======
import os

from bot import Bot

if __name__ == "__main__":
    token = os.environ['STRANGER_BOT_TOKEN']
    stranger_bot = Bot(bot_token=token)
>>>>>>> d7c565a81d20dd1a90d081523b8e0da2e9714b5d
