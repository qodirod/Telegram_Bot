from datetime import datetime

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.data.matches import MATCHES


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Schedule")],
        [KeyboardButton(text="My Bets")],
        [
            KeyboardButton(text="About this project"),
            KeyboardButton(text="Contact us")
        ],
        [
            KeyboardButton(text="Language"),
            KeyboardButton(text="Leaderboard")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose an option below"
)


mainru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Расписание")],
        [KeyboardButton(text="Мои ставки")],
        [
            KeyboardButton(text="О проекте"),
            KeyboardButton(text="Связаться с нами")
        ],
        [
            KeyboardButton(text="Язык"),
            KeyboardButton(text="Таблица лидеров")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите вариант ниже"
)


languages = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="English")],
        [KeyboardButton(text="Russian")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose a language"
)


def format_date_button(date_str: str, lang: str = "en") -> str:
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    if lang == "ru":
        months_ru = {
            1: "янв", 2: "фев", 3: "мар", 4: "апр",
            5: "май", 6: "июн", 7: "июл", 8: "авг",
            9: "сен", 10: "окт", 11: "ноя", 12: "дек"
        }
        return f"{date_obj.day} {months_ru[date_obj.month]}"

    return date_obj.strftime("%b %d")


def schedule_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    dates = sorted({match["date"] for match in MATCHES.values()})

    keyboard = []
    row = []

    for date_str in dates:
        row.append(
            InlineKeyboardButton(
                text=format_date_button(date_str, lang),
                callback_data=f"date:{date_str}"
            )
        )

        if len(row) == 3:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_team_name(match: dict, team_key: str, lang: str = "en") -> str:
    if lang == "ru":
        ru_key = f"{team_key}_ru"
        return match.get(ru_key, match.get(team_key, ""))

    return match.get(team_key, "")


def matches_by_date_keyboard(
    selected_date: str,
    lang: str = "en",
    get_countdown_func=None
) -> InlineKeyboardMarkup:
    keyboard = []

    for code, match in MATCHES.items():
        if match["date"] != selected_date:
            continue

        team1 = get_team_name(match, "team1", lang)
        team2 = get_team_name(match, "team2", lang)

        separator = "против" if lang == "ru" else "vs"

        countdown_text = ""
        if get_countdown_func:
            countdown = get_countdown_func(match["date"], match["time"], lang)
            countdown_text = f" ⏳ {countdown}"

        button_text = f'{match["time"]} — {team1} {separator} {team2}{countdown_text}'

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"match:{code}"
                )
            ]
        )

    back_text = "⬅️ Назад к датам" if lang == "ru" else "⬅️ Back to dates"

    keyboard.append(
        [
            InlineKeyboardButton(
                text=back_text,
                callback_data="back_to_dates"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def team_choice(
    game_code: str,
    team1: str,
    team2: str,
    team1_display: str = None,
    team2_display: str = None
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=team1_display or team1,
                    callback_data=f"bet:{game_code}:{team1}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=team2_display or team2,
                    callback_data=f"bet:{game_code}:{team2}"
                )
            ]
        ]
    )


def leaderboard_keyboard(users, lang: str = "en") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    medals = {
        1: "🥇",
        2: "🥈",
        3: "🥉"
    }

    for index, user in enumerate(users, start=1):
        medal = medals.get(index, "👤")

        name = user.first_name or user.username or f"User {user.tg_id}"
        balance = getattr(user, "balance", 100)

        builder.button(
            text=f"{medal} {index}. {name} — ${balance}",
            callback_data=f"profile:{user.tg_id}"
        )

    builder.adjust(1)

    return builder.as_markup()