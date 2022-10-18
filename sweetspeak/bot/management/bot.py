import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, executor

import config
from parser import SweetSpeakParser
from sweetspeak.bot.models import Bot

CHANNEL_ID = -1001516084523

# initialize the bot
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# initialize the parser
db = Bot.objects.all()
sweet_speak = SweetSpeakParser()

# initialize the scheduler
scheduler = AsyncIOScheduler()


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner


async def send_the_post_to_the_channel(channel_id: int, text: str):
    await bot.send_message(channel_id, text)


# check for the new article and do the feed
async def start_feed():
    if (sweet_speak.is_new_article()):
        sweet_speak.update_last_article_url()
        post = sweet_speak.make_a_post_from_the_article()
        await send_the_post_to_the_channel(CHANNEL_ID, post)


# start feed every day at 20:00
async def schedul():
    scheduler.add_job(start_feed, args=['job_date_once', ], id='job_date_once', trigger='date',
                      run_date='2018-04-05 07:48:05')
    scheduler.start()


async def on_startup(_):
    asyncio.create_task(schedul())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
