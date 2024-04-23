import asyncio
import logging
from aiogram import Bot, Dispatcher
import send_msg

dp = Dispatcher()
bot = Bot(token="BOT_TOKEN")


async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_routers(send_msg.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
