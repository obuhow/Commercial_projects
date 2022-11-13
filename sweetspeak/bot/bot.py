import telebot
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import time

from .config import API_TOKEN
from .parser import SweetSpeakParser
from .models import ScheduledPosts

# initialize the bot
bot = telebot.TeleBot(API_TOKEN)

# initialize the scheduler
scheduler = BackgroundScheduler()

# parse new articles
sweetspeak = SweetSpeakParser()
sweetspeak.make_new_posts()
db = ScheduledPosts.objects.all()

# start feed at scheduled time
def plan_feed():
    tz = pytz.timezone('Europe/Moscow')
    i = 1
    for feed in db:
        scheduler.add_job(bot.send_message, args=['@sweet_speak_test', feed.post],
                          id=f'job_date_once {i}', trigger='date',
                          run_date=feed.sending_datetime, timezone=tz)
        i += 1
    scheduler.start()

@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

plan_feed()

dblast = ScheduledPosts.objects.last()
bot.send_message(dblast.channel_id, text=dblast.post)

bot.polling(none_stop=True, interval=0)
