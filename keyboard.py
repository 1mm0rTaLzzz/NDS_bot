from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from math import ceil
import datetime

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

def q1_button_text():
    month = datetime.datetime.now().month
    if 2 <= month < 5:
        current_quarter = 2
    elif 5 <= month < 8:
        current_quarter = 3
    elif 8 <= month < 11:
        current_quarter = 4
    else:
        current_quarter = 1

    current_year = datetime.datetime.now().year
    button_text = f'{current_quarter} квартал {current_year}'

    return button_text


def q1():
    button_text = q1_button_text()

    q1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=button_text, callback_data="q1ans_1")],
                                           [InlineKeyboardButton(text='Прошедшие периоды', callback_data="q1ans_2")]])

    return q1



