import os

from bot import Bot

if __name__ == "__main__":
    token = os.environ['STRANGER_BOT_TOKEN']
    stranger_bot = Bot(bot_token=token)
