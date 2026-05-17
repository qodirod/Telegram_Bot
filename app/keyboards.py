from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Schedule')],
        [KeyboardButton(text='My Bets')],
        [
            KeyboardButton(text='About this project'),
            KeyboardButton(text='Contact us')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose an option below'
)

mainru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Расписание')],
        [KeyboardButton(text='Мои ставки')],
        [
            KeyboardButton(text='О проекте'),
            KeyboardButton(text='Связаться с нами')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите вариант ниже'
)

languages = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='English')],
        [KeyboardButton(text='Russian')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose a language'
)

schedule = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Jun 11, 3:00 p.m.", callback_data='MvSA')],
        [InlineKeyboardButton(text="Jun 11, 10:00 p.m.", callback_data='SKvC')],
        [InlineKeyboardButton(text="Jun 12, 3:00 p.m.", callback_data='CvBH')],
        [InlineKeyboardButton(text="Jun 12, 9:00 p.m.", callback_data='USvP')],
        [InlineKeyboardButton(text="Jun 13, 3:00 p.m.", callback_data='QvSW')],
        [InlineKeyboardButton(text="Jun 13, 6:00 p.m.", callback_data='BvM')],
        [InlineKeyboardButton(text="Jun 13, 9:00 p.m.", callback_data='HvS')],

        [InlineKeyboardButton(text="Jun 14", callback_data='AvT')],
        [InlineKeyboardButton(text="Jun 15", callback_data='SvCV')],
        [InlineKeyboardButton(text="Jun 16", callback_data='FvSe')],
        [InlineKeyboardButton(text="Jun 16", callback_data='FvSe')]

    ]
)