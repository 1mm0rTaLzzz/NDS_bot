import logging
import asyncio
from aiogram import Bot, Dispatcher
from core.settings import settings
from core.handlers import router



async def get_start(bot: Bot):
    await bot.send_message(settings.bots.admin_id, "Бот запущен!")



async def get_stop(bot: Bot):
    await bot.send_message(settings.bots.admin_id, "Бот остановлен!")



async def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    bot = Bot(settings.bots.bot_token)
    dp = Dispatcher()
    dp.startup.register(get_start)
    dp.shutdown.register(get_stop)
    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot turned off')