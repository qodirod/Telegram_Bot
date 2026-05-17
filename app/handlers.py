import os
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv

import app.keyboards as kb
import app.database.requests as rq

load_dotenv()
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '').split(',')))
ORGANIZER = os.getenv('ORGANIZER_USERNAME', '@organizer')

router = Router()


# ---------- Start & basics ----------
@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id,
                      username=message.from_user.username,
                      first_name=message.from_user.first_name)
    await message.answer(
        'Welcome! Please choose your language first.\n'
        'Добро пожаловать! Сначала выберите язык.',
        reply_markup=kb.languages
    )


# Language selection
@router.message(F.text.lower() == 'language')
@router.message(F.text.lower() == 'язык')
async def choose_language(message: Message):
    await message.answer(
        'Please choose your preferred language:',
        reply_markup=kb.languages
    )


@router.message(F.text.lower() == 'english')
async def set_english(message: Message):
    await rq.update_user_language(message.from_user.id, 'en')
    await message.answer('Language changed to English.', reply_markup=kb.main)


@router.message(F.text.lower() == 'russian')
async def set_russian(message: Message):
    await rq.update_user_language(message.from_user.id, 'ru')
    await message.answer('Язык изменён на русский.', reply_markup=kb.mainru)


# About and Contact
@router.message(F.text.lower() == 'about this project')
async def about_en(message: Message):
    await message.answer(
        'This project is a private FIFA World Cup 2026 prediction game for family and friends only.\n\n'
        'In this game, each participant chooses the team they believe will win. '
        'After the FIFA World Cup matches are completed, points will be calculated based on the results. '
        'The participant with the highest number of points will receive a gift.',
        reply_markup=kb.main
    )


@router.message(F.text.lower() == 'о проекте')
async def about_ru(message: Message):
    await message.answer(
        'Этот проект — частная игра-прогноз на Чемпионат мира по футболу FIFA 2026 '
        'только для семьи и друзей.\n\n'
        'В этой игре каждый участник выбирает команду, которая, по его мнению, победит. '
        'После завершения матчей Чемпионата мира очки будут подсчитаны на основе результатов. '
        'Участник, набравший наибольшее количество очков, получит подарок.',
        reply_markup=kb.mainru
    )


@router.message(F.text.lower() == 'contact us')
async def contact_en(message: Message):
    await message.answer(
        f'If you have any questions or need help, please contact the project organizer: {ORGANIZER}',
        reply_markup=kb.main
    )


@router.message(F.text.lower() == 'связаться с нами')
async def contact_ru(message: Message):
    await message.answer(
        f'Если у вас есть вопросы или вам нужна помощь, пожалуйста, свяжитесь с организатором проекта: {ORGANIZER}',
        reply_markup=kb.mainru
    )


# ---------- Schedule & predictions ----------
@router.message(F.text.lower() == 'schedule')
@router.message(F.text.lower() == 'расписание')
async def show_schedule(message: Message):
    await message.answer(
        'Please select a match for your prediction:',
        reply_markup=kb.schedule_keyboard()
    )


@router.callback_query(F.data == 'ignore')
async def ignore_callback(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data.startswith('match:'))
async def choose_match(callback: CallbackQuery):
    game_code = callback.data.split(':')[1]
    game = await rq.get_game_by_code(game_code)

    if not game:
        await callback.message.answer('Match not found.')
        await callback.answer()
        return

    await callback.message.answer(
        f'⚽ {game.team1} vs {game.team2}\n'
        f'📅 {game.match_date} at {game.match_time}\n\n'
        f'Please choose the team you believe will win:',
        reply_markup=kb.team_choice(game.code, game.team1, game.team2)
    )
    await callback.answer()


@router.callback_query(F.data.startswith('bet:'))
async def save_prediction(callback: CallbackQuery):
    _, game_code, selected_team = callback.data.split(':', 2)

    result = await rq.save_prediction(
        tg_id=callback.from_user.id,
        game_code=game_code,
        selected_team=selected_team
    )

    if result == 'exists':
        await callback.message.answer('You already made a prediction for this match.')
    elif result == 'saved':
        game = await rq.get_game_by_code(game_code)
        await callback.message.answer(
            f'✅ Your prediction has been saved.\n\n'
            f'Match: {game.team1} vs {game.team2}\n'
            f'Your choice: {selected_team}'
        )
    else:
        await callback.message.answer('Something went wrong. Please try again.')

    await callback.answer()


# ---------- My Bets ----------
@router.message(F.text.lower() == 'my bets')
@router.message(F.text.lower() == 'мои ставки')
async def my_bets(message: Message):
    predictions = await rq.get_user_predictions(message.from_user.id)
    if not predictions:
        lang = await rq.get_user_language(message.from_user.id)
        if lang == 'ru':
            await message.answer('У вас пока нет сохранённых прогнозов.', reply_markup=kb.mainru)
        else:
            await message.answer('You have no saved predictions yet.', reply_markup=kb.main)
        return

    text_lines = ['Your predictions:' if await rq.get_user_language(message.from_user.id) == 'en' else 'Ваши прогнозы:']
    for pred, game in predictions:
        pts = f" ({pred.points} pts)" if game.result else ""
        line = f"{game.team1} vs {game.team2} – {pred.selected_team}{pts}"
        text_lines.append(line)

    await message.answer('\n'.join(text_lines))


# ---------- Leaderboard ----------
@router.message(F.text.lower() == 'leaderboard')
@router.message(F.text.lower() == 'таблица лидеров')
async def leaderboard(message: Message):
    users = await rq.get_leaderboard()
    if not users:
        await message.answer('No scores yet.')
        return

    lines = ['🏆 Leaderboard:' if await rq.get_user_language(message.from_user.id) != 'ru' else '🏆 Таблица лидеров:']
    for idx, user in enumerate(users, start=1):
        name = user.first_name or user.username or f"User {user.tg_id}"
        lines.append(f"{idx}. {name} – {user.total_points} pts")

    await message.answer('\n'.join(lines))


# ---------- Admin commands ----------
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(Command(commands=['setresult']))
async def set_result_cmd(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer('You do not have permission to use this command.')
        return

    # Parse: /setresult GAME_CODE | WINNER | RESULT
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer('Usage: /setresult GAME_CODE | WINNER | RESULT\nExample: `/setresult MEX_RSA_0611_1500 | Mexico | 2-1`')
        return

    args = parts[1].split('|')
    if len(args) != 3:
        await message.answer('Invalid format. Use: /setresult GAME_CODE | WINNER | RESULT')
        return

    code = args[0].strip()
    winner = args[1].strip()
    result = args[2].strip()

    success = await rq.set_game_result(code, winner, result)
    if success:
        await message.answer(f'Result set: {code} – {winner} wins ({result}). Points recalculated.')
    else:
        await message.answer(f'Game with code {code} not found.')


@router.message(Command(commands=['leaderboard']))
async def leaderboard_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer('You do not have permission to use this command.')
        return
    await leaderboard(message)  # reuse the same handler logic
