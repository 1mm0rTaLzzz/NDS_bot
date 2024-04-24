from datetime import datetime, date
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import Message
from aiogram import Bot

from scheduler.db import get_users

from core.keyboard import comment

scheduler = AsyncIOScheduler()


async def bot_scheduled_notification(bot: Bot, user_id: int, message_text: str, reply_markup=None):
    await bot.send_message(
        user_id, message_text, reply_markup=reply_markup)

def add_bot_scheduled_notification(bot: Bot, user_id: int, date: datetime, message_text: str, reply_markup=None):
    scheduler.add_job(bot_scheduled_notification, 'date', run_date=date, kwargs={
                      'bot': bot, 'user_id': user_id, 'message_text': message_text, 'reply_markup': reply_markup})
    scheduler.start()


async def mailing(bot: Bot, message_text: str):
    users = get_users()

    for user in users:
        await bot.send_message(user[0], message_text)


def add_mailing(bot: Bot, date: datetime, message_text: str):
    scheduler.add_job(mailing, trigger='interval', weeks=13, start_date=date, kwargs={
                      'bot': bot, 'message_text': message_text})
    scheduler.start()