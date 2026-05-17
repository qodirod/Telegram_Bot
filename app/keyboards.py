from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from app.data.matches import MATCHES
from collections import defaultdict

# Main keyboards (reply)
main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Schedule')],
        [KeyboardButton(text='My Bets')],
        [
            KeyboardButton(text='About this project'),
            KeyboardButton(text='Contact us')
        ],
        [KeyboardButton(text='Language')],
        [KeyboardButton(text='Leaderboard')]
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
        ],
        [KeyboardButton(text='Язык')],
        [KeyboardButton(text='Таблица лидеров')]
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

# Inline keyboards
def schedule_keyboard() -> InlineKeyboardMarkup:
    """Generate inline keyboard with all matches grouped by date."""
    grouped = defaultdict(list)
    for code, info in MATCHES.items():
        grouped[info['date']].append((code, info))

    buttons = []
    # sort dates
    for date in sorted(grouped.keys()):
        # add a row with date as a header button (non-clickable)
        buttons.append([InlineKeyboardButton(text=f"{date}", callback_data='ignore')])
        for code, info in grouped[date]:
            text = f"{info['team1']} vs {info['team2']} ({info['time']})"
            buttons.append([InlineKeyboardButton(text=text, callback_data=f'match:{code}')])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def team_choice(game_code: str, team1: str, team2: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=team1, callback_data=f'bet:{game_code}:{team1}')],
            [InlineKeyboardButton(text=team2, callback_data=f'bet:{game_code}:{team2}')]
        ]
    )
