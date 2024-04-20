from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, Update, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from core.settings import settings
import logging

import core.keyboard as kb  # Importing custom keyboard markup

router = Router()
bot = Bot(settings.bots.bot_token)

class Register(StatesGroup):
    start_dialog = State()
    wait = State()
    comment = State()
    finish = State()
    question1 = State()
    check = State()


admin_id = int(settings.bots.admin_id)
user_id = None
permission_to_send_messages = False


@router.message(CommandStart())
async def get_start(message: Message, state: FSMContext):
    global user_id
    await message.answer('Здравствуйте! Ожидайте пока к диалогу подключается менеджер.')
    await bot.send_message(chat_id=settings.bots.admin_id, text=f'Заявка от {message.from_user.full_name}',
                           reply_markup=kb.get_start)
    await state.update_data(user_id=message.from_user.id)
    user_id = int(message.from_user.id)
    await state.set_state(Register.wait)


@router.message(Register.wait)
async def handle_messages(message: Message, state:FSMContext):
    data = await state.get_data()
    if data.get("wait"):
        await state.set_state(Register.start_dialog)

@router.message(Register.start_dialog)
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
        try:
            await bot.send_message(admin_id, f"Пользователь написал: {message.text}", reply_markup=kb.stop)
        except Exception as e:
            logging.exception(e)

    await state.set_state(Register.start_dialog)  # Устанавливаем состояние "start_dialog"


@router.callback_query(F.data == "Start dialog")
async def start_dialog_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Диалог начат.")
    await bot.send_message(chat_id=user_id, text="Диалог начат.")
    await state.set_state(Register.start_dialog)
    await state.update_data(wait=True)
    global permission_to_send_messages
    permission_to_send_messages = True


@router.callback_query(F.data == "Stop dialog")
async def start_dialog_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Диалог закончен.")
    await state.set_state(None)
