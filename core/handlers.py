from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from core.settings import settings

import core.keyboard as kb  # Importing custom keyboard markup

router = Router()
bot = Bot(settings.bots.bot_token)
user_to_admin = {}


class Register(StatesGroup):
    start_dialog = State()
    comment = State()


@router.message(CommandStart())
async def get_start(message: Message, state: FSMContext):
    await message.answer('Здравствуйте! Ответьте на пару вопросов пока к диалогу подключается менеджер.')
    await state.set_state(Register.start_dialog)
    await message.answer('Вопрос', reply_markup=kb.question1)
    await bot.send_message(chat_id=settings.bots.admin_id, text=f'Заявка от {message.from_user.full_name}',
                           reply_markup=kb.get_start)


# Обработка команды /start
@router.callback_query(F.data == "Start dialog")
async def start(message: Message, state: FSMContext):
    user_to_admin[message.from_user.id] = settings.bots.admin_id  # Сопоставляем ID пользователя с ID администратора
    await message.bot.send_message(chat_id=message.from_user.id,
                                   text="Вы начали чат с администратором. Отправьте своё сообщение.")
    await state.set_state(Register.start_dialog)


@router.message(Register.start_dialog)
async def handle_message(message: Message, state: FSMContext):
    if message.from_user.id in user_to_admin:
        await bot.send_message(settings.bots.admin_id,
                               f"Пользователь с ID {message.from_user.id} пишет: {message.text}", reply_markup=kb.stop)
        await message.reply("Ваше сообщение было успешно отправлено администратору.")
    else:
        await message.reply("Вы не начали беседу с администратором. Используйте команду /start, чтобы начать.")
    await state.set_state(Register.comment)


@router.message(Register.comment)
async def handle_admin_message(message: Message, state: FSMContext):
    for user_id, admin in user_to_admin.items():
        if admin == settings.bots.admin_id:
            await bot.send_message(user_id, f"Администратор отвечает: {message.text}", reply_markup=kb.stop)
    await state.set_state(Register.start_dialog)


@router.callback_query(F.data == "Stop")
async def stop_callback_query(callback:CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await state.clear()
