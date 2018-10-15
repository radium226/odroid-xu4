#!/usr/bin/env python

from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Server:

    def __init__(self, context):
        self.context = context

        self.bot = Bot(context.config["telegram"]["token"])
        self.updater = Updater(context.config["telegram"]["token"])

    def on_message_received(self, callback):
        def handler_callback(bot, update):
            callback(update.message.text)

        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, handler_callback))

    def send_message(self, text):
        self.bot.send_message(chat_id=self.context.config["telegram"]["chat_id"], text=text)

    def start(self):
        self.updater.start_polling()
