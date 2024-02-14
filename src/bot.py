import os
import telebot
from loguru import logger

BOT = telebot.TeleBot(
    os.environ['STRANGER_BOT_TOKEN']
)
logger.info('bot token is read!!!')