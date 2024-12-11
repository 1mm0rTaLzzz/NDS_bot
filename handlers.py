from datetime import timedelta
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, Update
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from core.settings import settings

from scheduler.scheduler import add_bot_scheduled_notification, add_notification_for_unanswered
from scheduler.strings import next_day_notification, not_answered_notification
from scheduler.db import create_user, update_user_status

import logging

import core.keyboard as kb  # Importing custom keyboard markup

router = Router()
bot = Bot(settings.bots.bot_token)

admin_id = int(settings.bots.admin_id)

client_chat_id = None  # ID чата клиента будет установлено при получении заявки
dialog_active = False  # Флаг активности диалога


class Questions(StatesGroup):
    question1 = State()
    question2 = State()
    comment = State()
    temp = State()


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    global client_chat_id
    client_chat_id = message.chat.id
    await bot.send_message(admin_id,
                           f"Получена новая заявка от {message.from_user.full_name}. Нажмите кнопку чтобы начать диалог.",
                           reply_markup=kb.get_start)
    await bot.send_message(client_chat_id,
                           "Здравствуйте! Пока к диалогу подключается менеджер, ответьте на два вопроса.")
    await bot.send_message(client_chat_id, "За какой период интересует оптимизация?", reply_markup=kb.q1())

    try:
        create_user(client_chat_id)
        add_bot_scheduled_notification(bot, client_chat_id, message.date + timedelta(days=1), next_day_notification, kb.comment) # Добавление задачи в планировщик для отправки сообщения через день
        add_notification_for_unanswered(bot, client_chat_id, message.date + timedelta(days=2), not_answered_notification)
    except Exception as e:
        print(e)


@router.callback_query(F.data.startswith("q1ans_"))
async def callbacks_num(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    await callback.message.edit_reply_markup()
    if action == "1":
        await state.update_data(question1=kb.q1_button_text())
    elif action == "2":
        await state.update_data(question1="Прошедшие периоды")
    await bot.send_message(client_chat_id, "Какой примерно объём закупок требуется для оптимизации?",
                           reply_markup=kb.q2)

@router.callback_query(F.data.startswith("q2ans_"))
async def callbacks_num(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    await callback.message.edit_reply_markup()
    if action == "1":
        await state.update_data(question2="от 0 до 10 млн")
    elif action == "2":
        await state.update_data(question2="от 10 до 50 млн")
    elif action == "3":
        await state.update_data(question2="от 50 до 100 млн")
    elif action == "4":
        await state.update_data(question2="более 100 млн")
    await callback.answer()
    data = await state.get_data()
    await bot.send_message(admin_id,
                           f'ответ от {callback.from_user.full_name}\n{data["question1"]}\n{data["question2"]}')
    await bot.send_message(client_chat_id,
                           f'Введённые данные\n{data["question1"]}\n{data["question2"]}')
    await bot.send_message(client_chat_id, "Спасибо за ответы! Менеджер скоро присоединится.")
    
    update_user_status(callback.from_user.id)


@router.callback_query(F.data.startswith("comment"))
async def callbacks_num(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    
    await bot.send_message(callback.from_user.id, 'Оставьте свой комментарий.')

    await state.set_state(Questions.comment)

@router.message(Questions.comment)
async def comment(message: Message, state: FSMContext):
    await bot.send_message(admin_id, f'Комментарий от {message.from_user.full_name}\n{message.text}')
    await bot.send_message(message.from_user.id, f'Ваш комментарий\n{message.text}')
    await bot.send_message(message.from_user.id, "Спасибо за комментарий!")
    
    await state.set_state(None)


@router.callback_query(F.data == "Start dialog")
async def start_dialog(callback: CallbackQuery):
    global dialog_active
    dialog_active = True
    await bot.send_message(admin_id,
                           "Диалог начат. Все, что вы напишете, будет отправлено клиенту. Нажмите кнопку чтобы закончить диалог.")
    await bot.send_message(client_chat_id, "Диалог начат. Все, что вы напишете, будет отправлено менеджеру.")
    await callback.message.edit_reply_markup()


@router.callback_query(F.data == "Stop dialog")
async def end_dialog(callback: CallbackQuery):
    global dialog_active
    dialog_active = False
    await bot.send_message(admin_id, "Диалог закончен.")
    await bot.send_message(client_chat_id, "Диалог закончен.")
    await callback.message.edit_reply_markup()


@router.message(Command('stop'))


@router.message()
async def forward_message(message: Message):
    global client_chat_id
    if dialog_active:
        if message.chat.id == admin_id and client_chat_id is not None:
            await bot.send_message(client_chat_id, message.text)
        elif message.chat.id == client_chat_id:
            await bot.send_message(admin_id, message.text, reply_markup=kb.stop)
