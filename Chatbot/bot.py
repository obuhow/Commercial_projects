import logging

import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types

from parser import SweetSpeak
import config

CHANNEL_NAME = '@sweet_speak_test'

# set the log level
logging.basicConfig(level=logging.INFO)

# initialize the bot
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# initialize the parser
sweet_speak = SweetSpeak(last_article_url.txt)

# check for new article and do the feed
async def long_polling():
    while True:
        await asyncio.sleep(10)

        current_link = sweet_speak.is_new_article()

        if (current_link):
            # if there is new article link send post
                with open(sg.download_image(nfo['image']), 'rb') as photo:
                    for s in subscriptions:
                        await bot.send_photo(
                            s[1],
                            photo,
                            caption=nfo['title'] + "\n" + "Оценка: " + nfo['score'] + "\n" + nfo['excerpt'] + "\n\n" +
                                    nfo['link'],
                            disable_notification=True
                        )

                sg.update_last_article_url()


if __name__ == '__main__':
    dp.loop.create_task(long_polling())
    executor.start_polling(dp, skip_updates=True)