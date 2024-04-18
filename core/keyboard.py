from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

get_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать диалог', callback_data="Start dialog")]
])
question1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ответ 1', callback_data="Pressed1"),InlineKeyboardButton(text='Ответ 2', callback_data="Pressed2")]
])
