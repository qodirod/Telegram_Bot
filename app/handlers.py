from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

import app.keyboards as kb
import app.database.requests as rq

router = Router()



@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Hello', reply_markup=kb.main)

@router.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer(f'Help panel: \n1. Main menu\n2. Check today games')

@router.message(F.text.lower() == 'schedule')
async def show_schedule(message:Message):
    await message.answer('Please choose a date for a bet below:', reply_markup=kb.schedule)
