from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from core.settings import settings
import logging

import core.keyboard as kb  # Importing custom keyboard markup

router = Router()
bot = Bot(settings.bots.bot_token)


class Register(StatesGroup):
    start_dialog = State()
    comment = State()

admin_id = int(settings.bots.admin_id)
user_id = None
@router.message()
async def handle_messages(message: Message, state: FSMContext):
    global user_id

    if message.from_user.id == admin_id:
        if user_id:
            try:
                await bot.send_message(user_id, f"Админ написал: {message.text}")
            except Exception as e:
                logging.exception(e)
        else:
            await message.reply("ID пользователя неизвестен. Пожалуйста, дождитесь сообщения от пользователя.")

    else:
        user_id = message.from_user.id
        try:
            await bot.send_message(admin_id, f"Пользователь написал: {message.text}")
        except Exception as e:
            logging.exception(e)
    await state.set_state(Register.start_dialog)