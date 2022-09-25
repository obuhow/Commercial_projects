import telebot
import time
import config

bot = telebot.TeleBot(config.access_token)
CHANNEL_NAME = '@sweet_speak_test'

# The database will be connected here
f = open('data/fun.txt', 'r', encoding='UTF-8')
jokes = f.read().split('\n')
f.close()

for joke in jokes:
    bot.send_message(CHANNEL_NAME, joke)
    time.sleep(30)
bot.send_message(CHANNEL_NAME, "Статьи закончились :-(")