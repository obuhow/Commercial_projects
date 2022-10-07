from aiogram import Bot, Dispatcher, executor, types
import asyncio

from parser import SweetSpeak
import config

CHANNEL_ID = -1001516084523

# initialize the bot
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# initialize the parser
sweet_speak = SweetSpeak('last_article_url.txt')

async def send_the_post_to_the_channel(channel_id: int, text: str):
    await bot.send_message(channel_id, text)


# check for the new article and do the feed
async def long_polling():
    await asyncio.sleep(18)
    while True:
        if (sweet_speak.is_new_article()):
            # wait 30 minutes for the author to form an article
            sweet_speak.update_last_article_url()
            post = sweet_speak.make_a_post_from_the_article()
            await send_the_post_to_the_channel(CHANNEL_ID, post)

async def on_startup(_):
    asyncio.create_task(long_polling())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)