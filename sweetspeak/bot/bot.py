import time
from datetime import datetime

import telebot
from apscheduler.schedulers.background import BackgroundScheduler

from .config import API_TOKEN, UPDATE_HOUR, UPDATE_MINUTE
from .parser import SweetSpeakParser
from .models import ScheduledPosts, PublishedPosts



# initialize the bot, scheduler, parser
bot = telebot.TeleBot(API_TOKEN)
scheduler = BackgroundScheduler(timezone="Europe/Moscow")
sweetspeak = SweetSpeakParser()
db = ScheduledPosts.objects.all()

def send_message(channel_id, post, url):
    print("Send Message")
    # send message and update databases
    bot.send_message(channel_id, post)
    published_post = ScheduledPosts.objects.get(url=url)
    sending_datetime = datetime.now()
    sending_datetime_string = sending_datetime.strftime('%Y-%m-%d %H:%M:%S'),
    PublishedPosts.objects.create(sending_datetime_p=sending_datetime_string,
                                  channel_id_p=published_post.channel_id,
                                  url_p=published_post.url, post_p=published_post.post,)
    published_post.delete()

def plan_feed():
    print("Plan feed")
    sweetspeak.make_new_posts()
    # start feed at scheduled time
    jobs = scheduler.get_jobs()
    for feed in db:
        repeat_task = 1
        for job in jobs:
            if feed.url == job.id:
                print("Found job")
                repeat_task = 0
        if repeat_task:
            print("Add job")
            scheduler.add_job(send_message, args=[feed.channel_id, feed.post, feed.url],
                              id=feed.url, trigger='date',
                              run_date=feed.sending_datetime)

def start_sheduler():
    print("Start sheduler")
    # update shedule with posts every day at certain time
    scheduler.add_job(plan_feed, id='start',
                      trigger='cron', hour=UPDATE_HOUR, minute=UPDATE_MINUTE)
    scheduler.start()

# start sheduler 
start_sheduler()
bot.polling(none_stop=True, interval=0)
