from aiogram import F, Router
import app.keyboards as kb
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

import app.keyboards as kb

router = Router()



@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Welcome!', reply_markup=kb.main)
    await message.answer(
        'Please do not share this Telegram bot with anyone. Access is limited to approved users only.'
    )


# English Schedule
@router.message(F.text.lower() == 'schedule')
async def show_schedule_english(message: Message):
    await message.answer(
        'Please select a date for your bet below:',
        reply_markup=kb.schedule
    )


# Russian Schedule
@router.message(F.text.lower() == 'расписание')
async def show_schedule_russian(message: Message):
    await message.answer(
        'Пожалуйста, выберите дату для вашей ставки ниже:',
        reply_markup=kb.schedule
    )


# English My Bets
@router.message(F.text.lower() == 'my bets')
async def my_bets_english(message: Message):
    await message.answer(
        'Here you will be able to see your bets.'
    )


# Russian My Bets
@router.message(F.text.lower() == 'мои ставки')
async def my_bets_russian(message: Message):
    await message.answer(
        'Здесь вы сможете увидеть свои ставки.'
    )


# English About
@router.message(F.text.lower() == 'about this project')
async def about_this_project_english_button(message: Message):
    await message.answer(
        'Please choose your preferred language:\n\n'
        '🇬🇧 English\n'
        '🇷🇺 Russian',
        reply_markup=kb.languages
    )


# Russian About
@router.message(F.text.lower() == 'о проекте')
async def about_this_project_russian_button(message: Message):
    await message.answer(
        'Пожалуйста, выберите предпочитаемый язык:\n\n'
        '🇬🇧 English\n'
        '🇷🇺 Russian',
        reply_markup=kb.languages
    )


# English language choice
@router.message(F.text.lower() == 'english')
async def about_project_english(message: Message):
    await message.answer(
        'This project is a private FIFA World Cup 2026 prediction game for family and friends only.\n\n'
        'In this game, each participant chooses the team they believe will win. '
        'After the FIFA World Cup matches are completed, points will be calculated based on the results. '
        'The participant with the highest number of points will receive a gift.',
        reply_markup=kb.main
    )


# Russian language choice
@router.message(F.text.lower() == 'russian')
async def about_project_russian(message: Message):
    await message.answer(
        'Этот проект — частная игра-прогноз на Чемпионат мира по футболу FIFA 2026 '
        'только для семьи и друзей.\n\n'
        'В этой игре каждый участник выбирает команду, которая, по его мнению, победит. '
        'После завершения матчей Чемпионата мира очки будут подсчитаны на основе результатов. '
        'Участник, набравший наибольшее количество очков, получит подарок.',
        reply_markup=kb.mainru
    )


# English Contact Us
@router.message(F.text.lower() == 'contact us')
async def contact_us_english(message: Message):
    await message.answer(
        'If you have any questions or need help, please contact the project organizer.',
        reply_markup=kb.main
    )


# Russian Contact Us
@router.message(F.text.lower() == 'связаться с нами')
async def contact_us_russian(message: Message):
    await message.answer(
        'Если у вас есть вопросы или вам нужна помощь, пожалуйста, свяжитесь с организатором проекта.',
        reply_markup=kb.mainru
    )