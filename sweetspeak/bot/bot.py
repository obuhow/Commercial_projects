import asyncio
from aiogram import Bot, Dispatcher, executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .config import API_TOKEN
from .parser import SweetSpeakParser
from .models import ScheduledPosts


# initialize the bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# initialize the parser
db = ScheduledPosts.objects.all()
sweetspeak = SweetSpeakParser()

# initialize the scheduler
scheduler = AsyncIOScheduler()

def log_errors(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner


async def send_the_post_to_the_channel(channel_id: int, text: str):
    await bot.send_message(channel_id, text)


# start feed at scheduled time
async def schedul():
    i = 1
    for feed in db:
        scheduler.add_job(send_the_post_to_the_channel(feed.channel_id, feed.post),
                          args=[f'job_date_once {i}', ], id=f'job_date_once {i}', trigger='date',
                          run_date=feed.sending_datetime)
        i += 1
    scheduler.start()


async def on_startup(_):
    asyncio.create_task(schedul())


executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
