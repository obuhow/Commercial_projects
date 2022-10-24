import telebot
from apscheduler.schedulers.background import BackgroundScheduler

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
    i = 1
    for feed in db:
        scheduler.add_job(bot.send_message(feed.channel_id, feed.post),
                          args=[f'job_date_once {i}', ], id=f'job_date_once {i}', trigger='date',
                          run_date=feed.sending_datetime)
        i += 1
    scheduler.start()

plan_feed()
