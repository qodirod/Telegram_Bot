from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Schedule')],
        [KeyboardButton(text='My Bets')],
        [
            KeyboardButton(text='About this project'),
            KeyboardButton(text='Contact us'),
            KeyboardButton(text='Language')
        ],
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
            KeyboardButton(text='Связаться с нами'),
            KeyboardButton(text='Язык')
        ],
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
        [
            InlineKeyboardButton(text="Jun 11", callback_data="date_2026_06_11"),
            InlineKeyboardButton(text="Jun 12", callback_data="date_2026_06_12"),
            InlineKeyboardButton(text="Jun 13", callback_data="date_2026_06_13")
        ],
        [
            InlineKeyboardButton(text="Jun 14", callback_data="date_2026_06_14"),
            InlineKeyboardButton(text="Jun 15", callback_data="date_2026_06_15"),
            InlineKeyboardButton(text="Jun 16", callback_data="date_2026_06_16")
        ],
        [
            InlineKeyboardButton(text="Jun 17", callback_data="date_2026_06_17"),
            InlineKeyboardButton(text="Jun 18", callback_data="date_2026_06_18"),
            InlineKeyboardButton(text="Jun 19", callback_data="date_2026_06_19")
        ],
        [
            InlineKeyboardButton(text="Jun 20", callback_data="date_2026_06_20"),
            InlineKeyboardButton(text="Jun 21", callback_data="date_2026_06_21"),
            InlineKeyboardButton(text="Jun 22", callback_data="date_2026_06_22")
        ],
        [
            InlineKeyboardButton(text="Jun 23", callback_data="date_2026_06_23"),
            InlineKeyboardButton(text="Jun 24", callback_data="date_2026_06_24"),
            InlineKeyboardButton(text="Jun 25", callback_data="date_2026_06_25")
        ],
        [
            InlineKeyboardButton(text="Jun 26", callback_data="date_2026_06_26"),
            InlineKeyboardButton(text="Jun 27", callback_data="date_2026_06_27")
        ]
    ]
)



schedule_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="11 июн", callback_data="date_2026_06_11"),
            InlineKeyboardButton(text="12 июн", callback_data="date_2026_06_12"),
            InlineKeyboardButton(text="13 июн", callback_data="date_2026_06_13")
        ],
        [
            InlineKeyboardButton(text="14 июн", callback_data="date_2026_06_14"),
            InlineKeyboardButton(text="15 июн", callback_data="date_2026_06_15"),
            InlineKeyboardButton(text="16 июн", callback_data="date_2026_06_16")
        ],
        [
            InlineKeyboardButton(text="17 июн", callback_data="date_2026_06_17"),
            InlineKeyboardButton(text="18 июн", callback_data="date_2026_06_18"),
            InlineKeyboardButton(text="19 июн", callback_data="date_2026_06_19")
        ],
        [
            InlineKeyboardButton(text="20 июн", callback_data="date_2026_06_20"),
            InlineKeyboardButton(text="21 июн", callback_data="date_2026_06_21"),
            InlineKeyboardButton(text="22 июн", callback_data="date_2026_06_22")
        ],
        [
            InlineKeyboardButton(text="23 июн", callback_data="date_2026_06_23"),
            InlineKeyboardButton(text="24 июн", callback_data="date_2026_06_24"),
            InlineKeyboardButton(text="25 июн", callback_data="date_2026_06_25")
        ],
        [
            InlineKeyboardButton(text="26 июн", callback_data="date_2026_06_26"),
            InlineKeyboardButton(text="27 июн", callback_data="date_2026_06_27")
        ]
    ]
)

