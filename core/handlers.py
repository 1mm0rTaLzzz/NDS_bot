from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, Update, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from core.settings import settings
import logging

import core.keyboard as kb  # Importing custom keyboard markup

router = Router()
bot = Bot(settings.bots.bot_token)

admin_id = int(settings.bots.admin_id)

client_chat_id = None  # ID чата клиента будет установлено при получении заявки
dialog_active = False  # Флаг активности диалога


@router.message(Command('start'))
async def start(message: Message):
    global client_chat_id
    client_chat_id = message.chat.id
    await bot.send_message(admin_id,
                           f"Получена новая заявка от {message.from_user.full_name}. Нажмите /start_dialog чтобы начать диалог.",
                           reply_markup=kb.get_start)
    await bot.send_message(client_chat_id, "Здравствуйте! Ожидайте пока к диалогу подключается менеджер.")


@router.callback_query(F.data == "Start dialog")
async def start_dialog(callback: CallbackQuery):
    global dialog_active
    dialog_active = True
    await bot.send_message(admin_id,
                           "Диалог начат. Все, что вы напишете, будет отправлено клиенту. Нажмите /end_dialog чтобы закончить диалог.")
    await bot.send_message(client_chat_id, "Диалог начат. Все, что вы напишете, будет отправлено менеджеру.")
    await callback.message.edit_reply_markup(None)


@router.callback_query(F.data == "Stop dialog")
async def end_dialog(callback: CallbackQuery):
    global dialog_active
    dialog_active = False
    await bot.send_message(admin_id, "Диалог закончен.")
    await bot.send_message(client_chat_id, "Диалог закончен.")
    await callback.message.edit_reply_markup(None)


@router.message()
async def forward_message(message: Message):
    global client_chat_id
    if dialog_active:
        if message.chat.id == admin_id and client_chat_id is not None:
            await bot.send_message(client_chat_id, message.text)
        elif message.chat.id == client_chat_id:
            await bot.send_message(admin_id, message.text, reply_markup=kb.stop)
