import telebot
import time
import config
from mysql.connector import connect, Error

CHANNEL_NAME = '@sweet_speak_test'
SENDING_TIME_RANGE = 86400
class Bot():
    def __init__(self):
        self.address = telebot.TeleBot(config.access_token)
    def start_channel_feed(self, db='article'):
        try:
            with connect(
                    host='localhost',
                    user=config.user_bd,
                    password=config.pass_bd,
                    database=db,
            ) as connection:
                select_article_query = "SELECT text FROM article"
                with connection.cursor() as cursor:
                    cursor.execute(select_article_query)
                    for text in cursor.fetchall():
                        self.send_article_from_base(text)
        except Error as e:
            print(e)

    def send_article_from_base(self, text):
        self.address.send_message(CHANNEL_NAME, text)
        time.sleep(SENDING_TIME_RANGE)

if __name__ == '__main__':
    bot = Bot()
    bot.start_channel_feed()
