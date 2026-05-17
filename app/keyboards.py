from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Schedule')],
                                    [KeyboardButton(text='My Bets')],
                                    [KeyboardButton(text='About this project'),
                                    KeyboardButton(text='Contact us')]],
                                resize_keyboard=True,
                                input_field_placeholder='Choose an option below')

schedule = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Jun 11", callback_data='MvSA')],
                                                [InlineKeyboardButton(text="Jun 12", callback_data='CvBH')],
                                                [InlineKeyboardButton(text="Jun 13", callback_data='QvSW')],
                                                [InlineKeyboardButton(text="Jun 14", callback_data='AvT')],
                                                [InlineKeyboardButton(text="Jun 15", callback_data='SvCV')],
                                                [InlineKeyboardButton(text="Jun 16", callback_data='FvSe')]])
