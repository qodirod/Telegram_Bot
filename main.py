import asyncio
from aiogram import Bot, Dispatcher, F


from app.handlers import router


async def main():
    bot = Bot(token='8887834947:AAHdjq0CU9soSG0xaVs2FAmg3nqpMe3yNyY')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
