from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

get_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать диалог', callback_data="Start dialog")]
])

stop = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Закончить диалог', callback_data="Stop dialog")]])
