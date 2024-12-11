from datetime import datetime, timedelta
import logging
import asyncio
from aiogram import Bot, Dispatcher
from core.settings import settings
from core.handlers import router
from scheduler.db import create_tables
from scheduler.scheduler import add_mailing
from scheduler.strings import six_day_notification, three_day_notification, last_chance_notification

from apscheduler.schedulers import SchedulerAlreadyRunningError

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
    dp.include_routers(router)

    create_tables()

    try:
        add_mailing(bot, datetime(2024, 4, 19, 12, 0, 0), six_day_notification)
        add_mailing(bot, datetime(2024, 4, 22, 12, 0, 0), three_day_notification)
        add_mailing(bot, datetime(2024, 1, 25, 11, 0, 0), last_chance_notification)
    except SchedulerAlreadyRunningError:
        pass

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot turned off')
