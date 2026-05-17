import asyncio
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import async_main
from app.database.requests import seed_games


load_dotenv()


async def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN is missing. Please add it to your .env file.")

    await async_main()
    await seed_games()

    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)

    # Helps avoid old webhook/pending update problems
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())