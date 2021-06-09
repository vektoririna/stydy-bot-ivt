from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ИВТ1(1)/19'),
            KeyboardButton(text='ИВТ1(2)/19'),
            KeyboardButton(text='ИВТ2/19')
        ]
    ],
    resize_keyboard=True
)
