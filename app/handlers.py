from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from datetime import datetime, timedelta

import app.keyboards as kb


router = Router()

# Saves user language while bot is running
user_languages = {}


def get_countdown(match_date: str, match_time_24: str, lang: str = "en") -> str:
    now = datetime.now()

    match_datetime = datetime.strptime(
        f"{match_date} {match_time_24}",
        "%Y-%m-%d %H:%M"
    )

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


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_languages[message.from_user.id] = "en"

    await message.answer("Welcome!", reply_markup=kb.main)
    await message.answer(
        "Please do not share this Telegram bot with anyone. Access is limited to approved users only."
    )


@router.message(F.text.lower() == "schedule")
async def show_schedule_english(message: Message):
    user_languages[message.from_user.id] = "en"

    await message.answer(
        "Please select a date for your prediction below:\n\n"
        "⚠️ Important: You can submit your prediction only once for each match, "
        "so please choose carefully.",
        reply_markup=kb.schedule
    )


@router.message(F.text.lower() == "расписание")
async def show_schedule_russian(message: Message):
    user_languages[message.from_user.id] = "ru"

    await message.answer(
        "Пожалуйста, выберите дату для вашего прогноза:\n\n"
        "⚠️ Важно: вы можете сделать прогноз только один раз на каждый матч, "
        "поэтому выбирайте внимательно.",
        reply_markup=kb.schedule_ru
    )


@router.message(F.text.lower() == "my bets")
async def my_bets_english(message: Message):
    user_languages[message.from_user.id] = "en"

    await message.answer(
        "Here you will be able to see your predictions.",
        reply_markup=kb.main
    )


@router.message(F.text.lower() == "мои ставки")
async def my_bets_russian(message: Message):
    user_languages[message.from_user.id] = "ru"

    await message.answer(
        "Здесь вы сможете увидеть свои прогнозы.",
        reply_markup=kb.mainru
    )


@router.message(F.text.lower() == "about this project")
async def about_project_english(message: Message):
    user_languages[message.from_user.id] = "en"

    await message.answer(
        "This project is a private FIFA World Cup 2026 prediction game for family and friends only.\n\n"
        "In this game, each participant chooses the team they believe will win. "
        "After the FIFA World Cup matches are completed, points will be calculated based on the results. "
        "The participant with the highest number of points will receive a gift.\n\n"
        "Voting opens 10 days before each match and closes 1 day before the match. "
        "After voting is closed, participants will no longer be able to choose a team for that match.\n\n"
        "⚠️ Each participant can submit only one prediction per match, so please choose carefully.",
        reply_markup=kb.main
    )


@router.message(F.text.lower() == "о проекте")
async def about_project_russian(message: Message):
    user_languages[message.from_user.id] = "ru"

    await message.answer(
        "Этот проект — частная игра-прогноз на Чемпионат мира по футболу FIFA 2026 "
        "только для семьи и друзей.\n\n"
        "В этой игре каждый участник выбирает команду, которая, по его мнению, победит. "
        "После завершения матчей Чемпионата мира очки будут подсчитаны на основе результатов. "
        "Участник, набравший наибольшее количество очков, получит подарок.\n\n"
        "Голосование открывается за 10 дней до каждого матча и закрывается за 1 день до матча. "
        "После закрытия голосования участники больше не смогут выбрать команду на этот матч.\n\n"
        "⚠️ Каждый участник может сделать только один прогноз на каждый матч, поэтому выбирайте внимательно.",
        reply_markup=kb.mainru
    )


@router.message(F.text.lower() == "language")
async def choose_language_english(message: Message):
    await message.answer(
        "Please choose your preferred language:",
        reply_markup=kb.languages
    )


@router.message(F.text.lower() == "язык")
async def choose_language_russian(message: Message):
    await message.answer(
        "Пожалуйста, выберите предпочитаемый язык:",
        reply_markup=kb.languages
    )


@router.message(F.text.lower() == "english")
async def set_language_english(message: Message):
    user_languages[message.from_user.id] = "en"

    await message.answer(
        "Language changed to English.",
        reply_markup=kb.main
    )


@router.message(F.text.lower() == "russian")
async def set_language_russian(message: Message):
    user_languages[message.from_user.id] = "ru"

    await message.answer(
        "Язык изменён на русский.",
        reply_markup=kb.mainru
    )


@router.message(F.text.lower() == "contact us")
async def contact_us_english(message: Message):
    user_languages[message.from_user.id] = "en"

    await message.answer(
        "If you have any questions or need help, please contact the project organizer.",
        reply_markup=kb.main
    )


@router.message(F.text.lower() == "связаться с нами")
async def contact_us_russian(message: Message):
    user_languages[message.from_user.id] = "ru"

    await message.answer(
        "Если у вас есть вопросы или вам нужна помощь, пожалуйста, свяжитесь с организатором проекта.",
        reply_markup=kb.mainru
    )


MATCH_ROWS = [
    ("MEX_RSA_0611_1500", "Mexico vs South Africa", "Мексика против ЮАР", "2026-06-11", "3:00 p.m.", "15:00"),
    ("KOR_CZE_0611_2200", "South Korea vs Czechia", "Южная Корея против Чехии", "2026-06-11", "10:00 p.m.", "22:00"),

    ("CAN_BIH_0612_1500", "Canada vs Bosnia and Herzegovina", "Канада против Боснии и Герцеговины", "2026-06-12", "3:00 p.m.", "15:00"),
    ("USA_PAR_0612_2100", "USA vs Paraguay", "США против Парагвая", "2026-06-12", "9:00 p.m.", "21:00"),

    ("QAT_SUI_0613_1500", "Qatar vs Switzerland", "Катар против Швейцарии", "2026-06-13", "3:00 p.m.", "15:00"),
    ("BRA_MAR_0613_1800", "Brazil vs Morocco", "Бразилия против Марокко", "2026-06-13", "6:00 p.m.", "18:00"),
    ("HAI_SCO_0613_2100", "Haiti vs Scotland", "Гаити против Шотландии", "2026-06-13", "9:00 p.m.", "21:00"),

    ("AUS_TUR_0614_0000", "Australia vs Türkiye", "Австралия против Турции", "2026-06-14", "12:00 a.m.", "00:00"),
    ("GER_CUR_0614_1300", "Germany vs Curacao", "Германия против Кюрасао", "2026-06-14", "1:00 p.m.", "13:00"),
    ("NED_JPN_0614_1600", "Netherlands vs Japan", "Нидерланды против Японии", "2026-06-14", "4:00 p.m.", "16:00"),
    ("CIV_ECU_0614_1900", "Ivory Coast vs Ecuador", "Кот-д’Ивуар против Эквадора", "2026-06-14", "7:00 p.m.", "19:00"),
    ("TUN_SWE_0614_2200", "Tunisia vs Sweden", "Тунис против Швеции", "2026-06-14", "10:00 p.m.", "22:00"),

    ("ESP_CPV_0615_1200", "Spain vs Cape Verde", "Испания против Кабо-Верде", "2026-06-15", "12:00 p.m.", "12:00"),
    ("BEL_EGY_0615_1500", "Belgium vs Egypt", "Бельгия против Египта", "2026-06-15", "3:00 p.m.", "15:00"),
    ("KSA_URU_0615_1800", "Saudi Arabia vs Uruguay", "Саудовская Аравия против Уругвая", "2026-06-15", "6:00 p.m.", "18:00"),
    ("IRN_NZL_0615_2100", "Iran vs New Zealand", "Иран против Новой Зеландии", "2026-06-15", "9:00 p.m.", "21:00"),

    ("FRA_SEN_0616_1500", "France vs Senegal", "Франция против Сенегала", "2026-06-16", "3:00 p.m.", "15:00"),
    ("IRQ_NOR_0616_1800", "Iraq vs Norway", "Ирак против Норвегии", "2026-06-16", "6:00 p.m.", "18:00"),
    ("ARG_ALG_0616_2100", "Argentina vs Algeria", "Аргентина против Алжира", "2026-06-16", "9:00 p.m.", "21:00"),

    ("AUT_JOR_0617_0000", "Austria vs Jordan", "Австрия против Иордании", "2026-06-17", "12:00 a.m.", "00:00"),
    ("POR_COD_0617_1300", "Portugal vs Congo DR", "Португалия против ДР Конго", "2026-06-17", "1:00 p.m.", "13:00"),
    ("ENG_CRO_0617_1600", "England vs Croatia", "Англия против Хорватии", "2026-06-17", "4:00 p.m.", "16:00"),
    ("GHA_PAN_0617_1900", "Ghana vs Panama", "Гана против Панамы", "2026-06-17", "7:00 p.m.", "19:00"),
    ("UZB_COL_0617_2200", "Uzbekistan vs Colombia", "Узбекистан против Колумбии", "2026-06-17", "10:00 p.m.", "22:00"),

    ("CZE_RSA_0618_1200", "Czechia vs South Africa", "Чехия против ЮАР", "2026-06-18", "12:00 p.m.", "12:00"),
    ("SUI_BIH_0618_1500", "Switzerland vs Bosnia and Herzegovina", "Швейцария против Боснии и Герцеговины", "2026-06-18", "3:00 p.m.", "15:00"),
    ("CAN_QAT_0618_1800", "Canada vs Qatar", "Канада против Катара", "2026-06-18", "6:00 p.m.", "18:00"),
    ("MEX_KOR_0618_2100", "Mexico vs South Korea", "Мексика против Южной Кореи", "2026-06-18", "9:00 p.m.", "21:00"),

    ("USA_AUS_0619_1500", "USA vs Australia", "США против Австралии", "2026-06-19", "3:00 p.m.", "15:00"),
    ("SCO_MAR_0619_1500", "Scotland vs Morocco", "Шотландия против Марокко", "2026-06-19", "3:00 p.m.", "15:00"),
    ("BRA_HAI_0619_2100", "Brazil vs Haiti", "Бразилия против Гаити", "2026-06-19", "9:00 p.m.", "21:00"),

    ("TUR_PAR_0620_0000", "Türkiye vs Paraguay", "Турция против Парагвая", "2026-06-20", "12:00 a.m.", "00:00"),
    ("NED_SWE_0620_1300", "Netherlands vs Sweden", "Нидерланды против Швеции", "2026-06-20", "1:00 p.m.", "13:00"),
    ("GER_CIV_0620_1600", "Germany vs Ivory Coast", "Германия против Кот-д’Ивуара", "2026-06-20", "4:00 p.m.", "16:00"),
    ("ECU_CUR_0620_2000", "Ecuador vs Curacao", "Эквадор против Кюрасао", "2026-06-20", "8:00 p.m.", "20:00"),

    ("TUN_JPN_0621_0000", "Tunisia vs Japan", "Тунис против Японии", "2026-06-21", "12:00 a.m.", "00:00"),
    ("ESP_KSA_0621_1200", "Spain vs Saudi Arabia", "Испания против Саудовской Аравии", "2026-06-21", "12:00 p.m.", "12:00"),
    ("BEL_IRN_0621_1500", "Belgium vs Iran", "Бельгия против Ирана", "2026-06-21", "3:00 p.m.", "15:00"),
    ("URU_CPV_0621_1800", "Uruguay vs Cape Verde", "Уругвай против Кабо-Верде", "2026-06-21", "6:00 p.m.", "18:00"),
    ("NZL_EGY_0621_2100", "New Zealand vs Egypt", "Новая Зеландия против Египта", "2026-06-21", "9:00 p.m.", "21:00"),

    ("ARG_AUT_0622_1300", "Argentina vs Austria", "Аргентина против Австрии", "2026-06-22", "1:00 p.m.", "13:00"),
    ("FRA_IRQ_0622_1700", "France vs Iraq", "Франция против Ирака", "2026-06-22", "5:00 p.m.", "17:00"),
    ("NOR_SEN_0622_2000", "Norway vs Senegal", "Норвегия против Сенегала", "2026-06-22", "8:00 p.m.", "20:00"),
    ("JOR_ALG_0622_2300", "Jordan vs Algeria", "Иордания против Алжира", "2026-06-22", "11:00 p.m.", "23:00"),

    ("POR_UZB_0623_1300", "Portugal vs Uzbekistan", "Португалия против Узбекистана", "2026-06-23", "1:00 p.m.", "13:00"),
    ("ENG_GHA_0623_1600", "England vs Ghana", "Англия против Ганы", "2026-06-23", "4:00 p.m.", "16:00"),
    ("PAN_CRO_0623_1900", "Panama vs Croatia", "Панама против Хорватии", "2026-06-23", "7:00 p.m.", "19:00"),
    ("COL_COD_0623_2200", "Colombia vs Congo DR", "Колумбия против ДР Конго", "2026-06-23", "10:00 p.m.", "22:00"),

    ("SUI_CAN_0624_1500", "Switzerland vs Canada", "Швейцария против Канады", "2026-06-24", "3:00 p.m.", "15:00"),
    ("BIH_QAT_0624_1500", "Bosnia and Herzegovina vs Qatar", "Босния и Герцеговина против Катара", "2026-06-24", "3:00 p.m.", "15:00"),
    ("BRA_SCO_0624_1800", "Brazil vs Scotland", "Бразилия против Шотландии", "2026-06-24", "6:00 p.m.", "18:00"),
    ("MAR_HAI_0624_1800", "Morocco vs Haiti", "Марокко против Гаити", "2026-06-24", "6:00 p.m.", "18:00"),
    ("MEX_CZE_0624_2100", "Mexico vs Czechia", "Мексика против Чехии", "2026-06-24", "9:00 p.m.", "21:00"),
    ("KOR_RSA_0624_2100", "South Korea vs South Africa", "Южная Корея против ЮАР", "2026-06-24", "9:00 p.m.", "21:00"),

    ("ECU_GER_0625_1600", "Ecuador vs Germany", "Эквадор против Германии", "2026-06-25", "4:00 p.m.", "16:00"),
    ("CUR_CIV_0625_1600", "Curacao vs Ivory Coast", "Кюрасао против Кот-д’Ивуара", "2026-06-25", "4:00 p.m.", "16:00"),
    ("TUN_NED_0625_1900", "Tunisia vs Netherlands", "Тунис против Нидерландов", "2026-06-25", "7:00 p.m.", "19:00"),
    ("JPN_SWE_0625_1900", "Japan vs Sweden", "Япония против Швеции", "2026-06-25", "7:00 p.m.", "19:00"),
    ("USA_TUR_0625_2200", "USA vs Türkiye", "США против Турции", "2026-06-25", "10:00 p.m.", "22:00"),
    ("PAR_AUS_0625_2200", "Paraguay vs Australia", "Парагвай против Австралии", "2026-06-25", "10:00 p.m.", "22:00"),

    ("NOR_FRA_0626_1500", "Norway vs France", "Норвегия против Франции", "2026-06-26", "3:00 p.m.", "15:00"),
    ("SEN_IRQ_0626_1500", "Senegal vs Iraq", "Сенегал против Ирака", "2026-06-26", "3:00 p.m.", "15:00"),
    ("URU_ESP_0626_2000", "Uruguay vs Spain", "Уругвай против Испании", "2026-06-26", "8:00 p.m.", "20:00"),
    ("CPV_KSA_0626_2000", "Cape Verde vs Saudi Arabia", "Кабо-Верде против Саудовской Аравии", "2026-06-26", "8:00 p.m.", "20:00"),
    ("NZL_BEL_0626_2300", "New Zealand vs Belgium", "Новая Зеландия против Бельгии", "2026-06-26", "11:00 p.m.", "23:00"),
    ("EGY_IRN_0626_2300", "Egypt vs Iran", "Египет против Ирана", "2026-06-26", "11:00 p.m.", "23:00"),

    ("PAN_ENG_0627_1700", "Panama vs England", "Панама против Англии", "2026-06-27", "5:00 p.m.", "17:00"),
    ("CRO_GHA_0627_1700", "Croatia vs Ghana", "Хорватия против Ганы", "2026-06-27", "5:00 p.m.", "17:00"),
    ("COL_POR_0627_1930", "Colombia vs Portugal", "Колумбия против Португалии", "2026-06-27", "7:30 p.m.", "19:30"),
    ("COD_UZB_0627_1930", "Congo DR vs Uzbekistan", "ДР Конго против Узбекистана", "2026-06-27", "7:30 p.m.", "19:30"),
    ("ARG_JOR_0627_2200", "Argentina vs Jordan", "Аргентина против Иордании", "2026-06-27", "10:00 p.m.", "22:00"),
    ("ALG_AUT_0627_2200", "Algeria vs Austria", "Алжир против Австрии", "2026-06-27", "10:00 p.m.", "22:00"),
]


matches = {
    callback_id: {
        "name": name,
        "name_ru": name_ru,
        "date": match_date,
        "time": time_en,
        "time_ru": time_ru,
    }
    for callback_id, name, name_ru, match_date, time_en, time_ru in MATCH_ROWS
}


@router.callback_query(F.data.startswith("date_"))
async def show_matches_by_date(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "en")

    selected_date = callback.data.replace("date_", "").replace("_", "-")
    date_matches = []

    for callback_id, match in matches.items():
        if match["date"] == selected_date:
            countdown = get_countdown(match["date"], match["time_ru"], lang)

            if lang == "ru":
                button_text = f'{match["time_ru"]} — {match["name_ru"]} ⏳ {countdown}'
            else:
                button_text = f'{match["time"]} — {match["name"]} ⏳ {countdown}'

            date_matches.append(
                [InlineKeyboardButton(text=button_text, callback_data=callback_id)]
            )

    if lang == "ru":
        date_matches.append(
            [InlineKeyboardButton(text="⬅️ Назад к датам", callback_data="back_to_dates")]
        )
        title = f'⚽ Матчи на {datetime.strptime(selected_date, "%Y-%m-%d").strftime("%d.%m.%Y")}:'
    else:
        date_matches.append(
            [InlineKeyboardButton(text="⬅️ Back to dates", callback_data="back_to_dates")]
        )
        title = f'⚽ Matches on {datetime.strptime(selected_date, "%Y-%m-%d").strftime("%B %d, %Y")}:'

    matches_keyboard = InlineKeyboardMarkup(inline_keyboard=date_matches)

    await callback.message.edit_text(
        title,
        reply_markup=matches_keyboard
    )

    await callback.answer()


@router.callback_query(F.data == "back_to_dates")
async def back_to_dates(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "en")

    if lang == "ru":
        await callback.message.edit_text(
            "Пожалуйста, выберите дату для вашего прогноза:",
            reply_markup=kb.schedule_ru
        )
    else:
        await callback.message.edit_text(
            "Please select a date for your prediction below:",
            reply_markup=kb.schedule
        )

    await callback.answer()


@router.callback_query(F.data.in_(matches.keys()))
async def choose_match(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "en")

    match = matches[callback.data]

    if lang == "ru":
        match_name = match["name_ru"]
        match_time = match["time_ru"]
    else:
        match_name = match["name"]
        match_time = match["time"]

    match_date = match["date"]
    countdown = get_countdown(match["date"], match["time_ru"], lang)

    today = datetime.now().date()
    match_day = datetime.strptime(match_date, "%Y-%m-%d").date()

    voting_open_day = match_day - timedelta(days=10)
    voting_close_day = match_day - timedelta(days=1)

    if today < voting_open_day:
        if lang == "ru":
            await callback.message.answer(
                f"⏳ Голосование ещё не открыто.\n\n"
                f"⚽ {match_name}\n"
                f"🕒 {match_time}\n"
                f"⏰ До матча: {countdown}\n\n"
                f"Голосование откроется: {voting_open_day.strftime('%d.%m.%Y')}.\n"
                f"Голосование закроется: {voting_close_day.strftime('%d.%m.%Y')}."
            )
        else:
            await callback.message.answer(
                f"⏳ Voting is not open yet.\n\n"
                f"⚽ {match_name}\n"
                f"🕒 {match_time}\n"
                f"⏰ Countdown: {countdown}\n\n"
                f"Voting opens on {voting_open_day.strftime('%B %d, %Y')}.\n"
                f"Voting closes on {voting_close_day.strftime('%B %d, %Y')}."
            )

        await callback.answer()
        return

    if today >= voting_close_day:
        if lang == "ru":
            await callback.message.answer(
                f"❌ Голосование закрыто.\n\n"
                f"⚽ {match_name}\n"
                f"🕒 {match_time}\n\n"
                f"Голосование закрылось: {voting_close_day.strftime('%d.%m.%Y')}.\n"
                f"Выбор команды больше недоступен."
            )
        else:
            await callback.message.answer(
                f"❌ Voting is closed.\n\n"
                f"⚽ {match_name}\n"
                f"🕒 {match_time}\n\n"
                f"Voting closed on {voting_close_day.strftime('%B %d, %Y')}.\n"
                f"Team selection is no longer available."
            )

        await callback.answer()
        return

    if lang == "ru":
        await callback.message.answer(
            f"✅ Голосование открыто!\n\n"
            f"⚽ {match_name}\n"
            f"🕒 {match_time}\n"
            f"⏰ До матча: {countdown}\n\n"
            f"Голосование закроется: {voting_close_day.strftime('%d.%m.%Y')}.\n\n"
            f"Пожалуйста, выберите команду, которая, по вашему мнению, победит."
        )
    else:
        await callback.message.answer(
            f"✅ Voting is open!\n\n"
            f"⚽ {match_name}\n"
            f"🕒 {match_time}\n"
            f"⏰ Countdown: {countdown}\n\n"
            f"Voting closes on {voting_close_day.strftime('%B %d, %Y')}.\n\n"
            f"Please choose the team you believe will win."
        )

    await callback.answer()



@router.message(F.text.lower() == "farizcool")
async def fariz_cool_secret(message: Message):
    sticker_ids = [
        "CAACAgIAAxkBAAIBTmoJOgkmoRd3wFtXqJ_GB7rMW3EWAALxYAAC5uRASNAIcIz-f3sSOwQ",
        "CAACAgIAAxkBAAIBUWoJOohpxFMnuNTYe0DtMLnUHEpYAAKulAACn7HZSqZxEME-IlJoOwQ",
        "CAACAgIAAxkBAAIBU2oJOpwJrl27_0B0Tr4NiVSOzdAqAAL6aAACjCMxSA8aopIdneDoOwQ",
        "CAACAgIAAxkBAAIBVWoJOqk-yDqnwgyngYt8V2mU8n96AAKREwACTBoxSTWapkvzylkDOwQ",
        "CAACAgQAAxkBAAIBV2oJOsvwEucINhHSVIG21WzAz2XjAAKnCAAC_b5AUDCw_PIbqEVPOwQ"    ]

    await message.answer("😎 Secret code activated! Fariz is cool!")

    for sticker_id in sticker_ids:
        await message.answer_sticker(sticker_id)
