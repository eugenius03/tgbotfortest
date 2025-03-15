import asyncio
import logging
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, loggers
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from db.engine import create_tables
from routers import command_router, inline_router, message_router



async def main():

    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    bot_token = getenv("BOT_TOKEN")
    bot = Bot(bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    await create_tables()
    dp.include_router(command_router)
    dp.include_router(inline_router)
    dp.include_router(message_router)


    logging.info("Bot started")
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        handlers=[logging.FileHandler("bot.log", encoding="utf-8")]
    )
    logging.getLogger("aiogram").setLevel(logging.ERROR)

    asyncio.run(main())