from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

get_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать диалог', callback_data="Start dialog")]
])

stop = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Закончить диалог', callback_data="Stop dialog")]])
q1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='1 квартал 2024', callback_data="q1ans_1")],
                                           [InlineKeyboardButton(text='Прошедшие периоды', callback_data="q1ans_2")]])

q2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='от 0 до 10 млн', callback_data="q2ans_1")],
                                           [InlineKeyboardButton(text='от 10 до 50 млн', callback_data="q2ans_2")],
                                           [InlineKeyboardButton(text='от 50 до 100 млн', callback_data="q2ans_3")],
                                           [InlineKeyboardButton(text='более 100 млн', callback_data="q2ans_4")]])

comment = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Оставить комментарий', callback_data="comment")]])