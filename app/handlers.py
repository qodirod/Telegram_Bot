import os
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv

import app.keyboards as kb
import app.database.requests as rq
from app.data.matches import MATCHES


load_dotenv()

ADMIN_IDS = [
    int(admin_id)
    for admin_id in os.getenv("ADMIN_IDS", "").split(",")
    if admin_id.strip().isdigit()
]

ORGANIZER = os.getenv("ORGANIZER_USERNAME", "@organizer")

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def get_lang(user_id: int) -> str:
    lang = await rq.get_user_language(user_id)
    return lang if lang in ("en", "ru") else "en"


def get_main_keyboard(lang: str):
    return kb.mainru if lang == "ru" else kb.main


def parse_match_time(match_time: str) -> str:
    time_text = str(match_time).strip().lower()

    time_text = time_text.replace("a.m.", "AM")
    time_text = time_text.replace("p.m.", "PM")
    time_text = time_text.replace("am", "AM")
    time_text = time_text.replace("pm", "PM")
    time_text = time_text.replace(" ", "")

    try:
        return datetime.strptime(time_text, "%I:%M%p").strftime("%H:%M")
    except ValueError:
        pass

    try:
        return datetime.strptime(str(match_time).strip(), "%H:%M").strftime("%H:%M")
    except ValueError:
        return "00:00"


def get_match_datetime(match_date: str, match_time: str) -> datetime:
    time_24 = parse_match_time(match_time)

    return datetime.strptime(
        f"{match_date} {time_24}",
        "%Y-%m-%d %H:%M"
    )


def get_countdown(match_date: str, match_time: str, lang: str = "en") -> str:
    now = datetime.now()
    match_datetime = get_match_datetime(match_date, match_time)

    difference = match_datetime - now

    if difference.total_seconds() <= 0:
        return "начался" if lang == "ru" else "started"

    days = difference.days
    hours = difference.seconds // 3600
    minutes = (difference.seconds % 3600) // 60

    if lang == "ru":
        if days > 0:
            return f"{days}д {hours}ч"
        if hours > 0:
            return f"{hours}ч {minutes}м"
        return f"{minutes}м"

    if days > 0:
        return f"{days}d {hours}h"
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def match_has_started(match_date: str, match_time: str) -> bool:
    return datetime.now() >= get_match_datetime(match_date, match_time)


def get_match_info(code: str):
    return MATCHES.get(code)


def get_match_day(code: str):
    match = get_match_info(code)

    if not match:
        return None

    return datetime.strptime(match["date"], "%Y-%m-%d").date()


def get_display_team(match: dict, team_key: str, lang: str = "en") -> str:
    if lang == "ru":
        return match.get(f"{team_key}_ru", match.get(team_key, ""))

    return match.get(team_key, "")


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(
        message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )

    await message.answer(
        "Welcome! Please choose your language first.\n"
        "Добро пожаловать! Сначала выберите язык.",
        reply_markup=kb.languages
    )


@router.message(F.text.lower() == "language")
@router.message(F.text.lower() == "язык")
async def choose_language(message: Message):
    lang = await get_lang(message.from_user.id)

    if lang == "ru":
        await message.answer(
            "Пожалуйста, выберите предпочитаемый язык:",
            reply_markup=kb.languages
        )
    else:
        await message.answer(
            "Please choose your preferred language:",
            reply_markup=kb.languages
        )


@router.message(F.text.lower() == "english")
async def set_english(message: Message):
    await rq.update_user_language(message.from_user.id, "en")
    await message.answer("Language changed to English.", reply_markup=kb.main)


@router.message(F.text.lower() == "russian")
async def set_russian(message: Message):
    await rq.update_user_language(message.from_user.id, "ru")
    await message.answer("Язык изменён на русский.", reply_markup=kb.mainru)


@router.message(F.text.lower() == "about this project")
async def about_en(message: Message):
    await rq.update_user_language(message.from_user.id, "en")

    await message.answer(
        "This project is a private FIFA World Cup 2026 prediction game for family and friends only.\n\n"
        "Each player starts with $100. For every correct prediction, you get +$1. "
        "For every wrong prediction, you get -$1.\n\n"
        "Voting is available before each match, but it closes 1 day before the match. "
        "After voting is closed, participants will no longer be able to choose a team for that match.\n\n"
        "⚠️ Each participant can submit only one prediction per match, so please choose carefully.",
        reply_markup=kb.main
    )


@router.message(F.text.lower() == "о проекте")
async def about_ru(message: Message):
    await rq.update_user_language(message.from_user.id, "ru")

    await message.answer(
        "Этот проект — частная игра-прогноз на Чемпионат мира по футболу FIFA 2026 "
        "только для семьи и друзей.\n\n"
        "Каждый игрок начинает со $100. За правильный прогноз вы получаете +$1. "
        "За неправильный прогноз вы получаете -$1.\n\n"
        "Голосование доступно до каждого матча, но закрывается за 1 день до матча. "
        "После закрытия голосования участники больше не смогут выбрать команду на этот матч.\n\n"
        "⚠️ Каждый участник может сделать только один прогноз на каждый матч, поэтому выбирайте внимательно.",
        reply_markup=kb.mainru
    )


@router.message(F.text.lower() == "contact us")
async def contact_en(message: Message):
    await rq.update_user_language(message.from_user.id, "en")

    await message.answer(
        f"If you have any questions or need help, please contact the project organizer: {ORGANIZER}",
        reply_markup=kb.main
    )


@router.message(F.text.lower() == "связаться с нами")
async def contact_ru(message: Message):
    await rq.update_user_language(message.from_user.id, "ru")

    await message.answer(
        f"Если у вас есть вопросы или вам нужна помощь, пожалуйста, свяжитесь с организатором проекта: {ORGANIZER}",
        reply_markup=kb.mainru
    )


@router.message(F.text.lower() == "schedule")
async def show_schedule_en(message: Message):
    await rq.update_user_language(message.from_user.id, "en")

    await message.answer(
        "Please select a date for your prediction below:\n\n"
        "⚠️ Voting closes 1 day before each match.\n"
        "You can submit your prediction only once for each match, so please choose carefully.",
        reply_markup=kb.schedule_keyboard(lang="en")
    )


@router.message(F.text.lower() == "расписание")
async def show_schedule_ru(message: Message):
    await rq.update_user_language(message.from_user.id, "ru")

    await message.answer(
        "Пожалуйста, выберите дату для вашего прогноза:\n\n"
        "⚠️ Голосование закрывается за 1 день до каждого матча.\n"
        "Вы можете сделать прогноз только один раз на каждый матч, поэтому выбирайте внимательно.",
        reply_markup=kb.schedule_keyboard(lang="ru")
    )


@router.callback_query(F.data.startswith("date:"))
async def show_matches_by_date(callback: CallbackQuery):
    lang = await get_lang(callback.from_user.id)
    selected_date = callback.data.split(":", 1)[1]

    if lang == "ru":
        title = f"⚽ Матчи на {datetime.strptime(selected_date, '%Y-%m-%d').strftime('%d.%m.%Y')}:"
    else:
        title = f"⚽ Matches on {datetime.strptime(selected_date, '%Y-%m-%d').strftime('%B %d, %Y')}:"

    await callback.message.edit_text(
        title,
        reply_markup=kb.matches_by_date_keyboard(
            selected_date=selected_date,
            lang=lang,
            get_countdown_func=get_countdown
        )
    )

    await callback.answer()


@router.callback_query(F.data == "back_to_dates")
async def back_to_dates(callback: CallbackQuery):
    lang = await get_lang(callback.from_user.id)

    if lang == "ru":
        await callback.message.edit_text(
            "Пожалуйста, выберите дату для вашего прогноза:",
            reply_markup=kb.schedule_keyboard(lang="ru")
        )
    else:
        await callback.message.edit_text(
            "Please select a date for your prediction below:",
            reply_markup=kb.schedule_keyboard(lang="en")
        )

    await callback.answer()


@router.callback_query(F.data.startswith("match:"))
async def choose_match(callback: CallbackQuery):
    lang = await get_lang(callback.from_user.id)
    game_code = callback.data.split(":", 1)[1]

    game = await rq.get_game_by_code(game_code)
    match = get_match_info(game_code)

    if not game or not match:
        await callback.message.answer("Матч не найден." if lang == "ru" else "Match not found.")
        await callback.answer()
        return

    match_day = get_match_day(game_code)
    today = datetime.now().date()

    voting_close_day = match_day - timedelta(days=1)

    team1_display = get_display_team(match, "team1", lang)
    team2_display = get_display_team(match, "team2", lang)

    separator = "против" if lang == "ru" else "vs"
    countdown = get_countdown(match["date"], match["time"], lang)

    if today >= voting_close_day or match_has_started(match["date"], match["time"]):
        await callback.message.answer(
            (
                f"❌ Голосование закрыто.\n\n"
                f"⚽ {team1_display} {separator} {team2_display}\n"
                f"🕒 {match['time']}\n\n"
                f"Выбор команды больше недоступен."
            )
            if lang == "ru"
            else (
                f"❌ Voting is closed.\n\n"
                f"⚽ {team1_display} {separator} {team2_display}\n"
                f"🕒 {match['time']}\n\n"
                f"Team selection is no longer available."
            )
        )
        await callback.answer()
        return

    await callback.message.answer(
        (
            f"✅ Голосование открыто!\n\n"
            f"⚽ {team1_display} {separator} {team2_display}\n"
            f"📅 {match['date']}\n"
            f"🕒 {match['time']}\n"
            f"⏰ До матча: {countdown}\n\n"
            f"⚠️ Вы можете выбрать команду только один раз, поэтому выбирайте внимательно.\n\n"
            f"Выберите команду, которая, по вашему мнению, победит:"
        )
        if lang == "ru"
        else (
            f"✅ Voting is open!\n\n"
            f"⚽ {team1_display} {separator} {team2_display}\n"
            f"📅 {match['date']}\n"
            f"🕒 {match['time']}\n"
            f"⏰ Countdown: {countdown}\n\n"
            f"⚠️ You can choose only once, so please choose carefully.\n\n"
            f"Please choose the team you believe will win:"
        ),
        reply_markup=kb.team_choice(
            game.code,
            game.team1,
            game.team2,
            team1_display=team1_display,
            team2_display=team2_display
        )
    )

    await callback.answer()


@router.callback_query(F.data.startswith("bet:"))
async def save_prediction(callback: CallbackQuery):
    lang = await get_lang(callback.from_user.id)

    _, game_code, selected_team = callback.data.split(":", 2)

    game = await rq.get_game_by_code(game_code)
    match = get_match_info(game_code)

    if not game or not match:
        await callback.message.answer("Матч не найден." if lang == "ru" else "Match not found.")
        await callback.answer()
        return

    match_day = get_match_day(game_code)
    today = datetime.now().date()

    voting_close_day = match_day - timedelta(days=1)

    if today >= voting_close_day or match_has_started(match["date"], match["time"]):
        await callback.message.answer(
            "❌ Голосование уже закрыто. Выбор команды больше недоступен."
            if lang == "ru"
            else "❌ Voting is already closed. Team selection is no longer available."
        )
        await callback.answer()
        return

    result = await rq.save_prediction(
        tg_id=callback.from_user.id,
        game_code=game_code,
        selected_team=selected_team
    )

    team1_display = get_display_team(match, "team1", lang)
    team2_display = get_display_team(match, "team2", lang)
    separator = "против" if lang == "ru" else "vs"

    if result == "exists":
        await callback.message.answer(
            "⚠️ Вы уже сделали прогноз на этот матч. Можно выбрать только один раз."
            if lang == "ru"
            else "⚠️ You already made a prediction for this match. You can choose only once."
        )

    elif result == "saved":
        await callback.message.answer(
            (
                f"✅ Ваш прогноз сохранён.\n\n"
                f"Матч: {team1_display} {separator} {team2_display}\n"
                f"Ваш выбор: {selected_team}"
            )
            if lang == "ru"
            else (
                f"✅ Your prediction has been saved.\n\n"
                f"Match: {team1_display} {separator} {team2_display}\n"
                f"Your choice: {selected_team}"
            )
        )

    else:
        await callback.message.answer(
            "Что-то пошло не так. Пожалуйста, попробуйте ещё раз."
            if lang == "ru"
            else "Something went wrong. Please try again."
        )

    await callback.answer()


@router.message(F.text.lower() == "my bets")
@router.message(F.text.lower() == "мои ставки")
async def my_bets(message: Message):
    lang = await get_lang(message.from_user.id)
    predictions = await rq.get_user_predictions(message.from_user.id)

    if not predictions:
        await message.answer(
            "У вас пока нет сохранённых прогнозов."
            if lang == "ru"
            else "You have no saved predictions yet.",
            reply_markup=get_main_keyboard(lang)
        )
        return

    text_lines = ["Ваши прогнозы:" if lang == "ru" else "Your predictions:"]

    for pred, game in predictions:
        if game.result:
            money = f" ({pred.points}$)"
        else:
            money = ""

        line = f"{game.team1} vs {game.team2} — {pred.selected_team}{money}"
        text_lines.append(line)

    await message.answer("\n".join(text_lines), reply_markup=get_main_keyboard(lang))


@router.message(F.text.lower() == "leaderboard")
@router.message(F.text.lower() == "таблица лидеров")
async def leaderboard(message: Message):
    lang = await get_lang(message.from_user.id)
    users = await rq.get_leaderboard()

    if not users:
        await message.answer(
            "Пока нет игроков." if lang == "ru" else "No players yet.",
            reply_markup=get_main_keyboard(lang)
        )
        return

    text = (
        "🏆 Денежная таблица лидеров FIFA 2026\n\n"
        "Нажмите на игрока, чтобы открыть профиль:"
        if lang == "ru"
        else
        "🏆 FIFA 2026 Money Leaderboard\n\n"
        "Tap a player to open their profile:"
    )

    await message.answer(
        text,
        reply_markup=kb.leaderboard_keyboard(users, lang)
    )


@router.callback_query(F.data.startswith("profile:"))
async def open_user_profile(callback: CallbackQuery):
    lang = await get_lang(callback.from_user.id)

    tg_id = int(callback.data.split(":")[1])
    user = await rq.get_user_by_tg_id(tg_id)

    if not user:
        await callback.answer(
            "Пользователь не найден." if lang == "ru" else "User not found.",
            show_alert=True
        )
        return

    predictions = await rq.get_user_predictions(tg_id)

    name = user.first_name or user.username or f"User {user.tg_id}"
    username = f"@{user.username}" if user.username else "No username"

    text = (
        f"👤 Профиль игрока\n\n"
        f"Имя: {name}\n"
        f"Username: {username}\n"
        f"Баланс: ${user.balance}\n"
        f"Прогнозов: {len(predictions)}"
        if lang == "ru"
        else
        f"👤 Player Profile\n\n"
        f"Name: {name}\n"
        f"Username: {username}\n"
        f"Balance: ${user.balance}\n"
        f"Predictions: {len(predictions)}"
    )

    await callback.message.answer(text)
    await callback.answer()


@router.message(Command(commands=["setresult"]))
async def set_result_cmd(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("You do not have permission to use this command.")
        return

    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer(
            "Usage:\n"
            "/setresult GAME_CODE | WINNER | RESULT\n\n"
            "Example:\n"
            "/setresult MEX_RSA_0611_1500 | Mexico | 2-1"
        )
        return

    args = parts[1].split("|")

    if len(args) != 3:
        await message.answer("Invalid format. Use: /setresult GAME_CODE | WINNER | RESULT")
        return

    code = args[0].strip()
    winner = args[1].strip()
    result = args[2].strip()

    success = await rq.set_game_result(code, winner, result)

    if success:
        await message.answer(f"Result set: {code} — {winner} wins ({result}). Money recalculated.")
    else:
        await message.answer(f"Game with code {code} not found.")


@router.message(Command(commands=["leaderboard"]))
async def leaderboard_admin(message: Message):
    await leaderboard(message)


@router.message(F.text.lower() == "farizcool")
async def fariz_cool_secret(message: Message):
    sticker_ids = [
        "CAACAgIAAxkBAAIBTmoJOgkmoRd3wFtXqJ_GB7rMW3EWAALxYAAC5uRASNAIcIz-f3sSOwQ",
        "CAACAgIAAxkBAAIBUWoJOohpxFMnuNTYe0DtMLnUHEpYAAKulAACn7HZSqZxEME-IlJoOwQ",
        "CAACAgIAAxkBAAIBU2oJOpwJrl27_0B0Tr4NiVSOzdAqAAL6aAACjCMxSA8aopIdneDoOwQ",
        "CAACAgIAAxkBAAIBVWoJOqk-yDqnwgyngYt8V2mU8n96AAKREwACTBoxSTWapkvzylkDOwQ",
        "CAACAgQAAxkBAAIBV2oJOsvwEucINhHSVIG21WzAz2XjAAKnCAAC_b5AUDCw_PIbqEVPOwQ",
    ]

    await message.answer("😎 Secret code activated! Fariz is cool!")

    for sticker_id in sticker_ids:
        await message.answer_sticker(sticker_id)