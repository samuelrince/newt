import os
import telegram.ext

from telegram.ext import Updater

from src.article import Article


class Bot:

    def __init__(self):
        self.__updater = Updater(os.environ['BOT_TOKEN'], use_context=True)
        self.__job_queue = self.__updater.job_queue

    def send_article(self, article: Article, channel_name: str):
        pass
