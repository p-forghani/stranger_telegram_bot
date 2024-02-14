import pymongo
import os
from loguru import logger

client = pymongo.MongoClient('localhost', port=27017)
db = client.stranger_telegram_bot
logger.info("db.py imported...")
