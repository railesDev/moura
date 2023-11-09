from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_reader import config
import json
import asyncio
import logging
import sys
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from os import getenv
from typing import Any, Dict
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# ADD CHECKS THAT ALL PREVIOUS ARE FILLED
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from aiogram.enums import ParseMode
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.enums import ParseMode

import sqlite3

logging.basicConfig(level=logging.INFO)

# Connect to the SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create the users table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, gender integer, campus text, program text, course integer, goals text, ad_text text)''')


# Configure bot
storage = MemoryStorage()
moura = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)


# Configure our user profile
class Form(StatesGroup):
    id = State()
    gender = State()
    campus = State()
    program = State()
    course = State()
    goals = State()
    ad_text = State()
    unfinished = State()


answers_dict = {"gender": ['I am a Guy ‍👨‍💼', 'I am a Lady ‍👩‍💼'], "campus": ['Kantemirovskaya 🏭', 'Griboedova 🏨', 'Promyshlennaya 🏫', 'Sedova 🏠'],
           "program": ['Logistics 🚚', 'InterBusiness 💼', 'Economics 📈', 'InterBac 🤹‍', 'PMI 💻', 'Data Analytics 📊', 'Physics 🌌', 'Law ⚖️',
                       'History 📜', 'Mediacommunications 📱', 'Philology 📚', 'Politology 🏛️', 'Vostokovedenie ⛩️', 'Design 🎨', 'UAGS 🏢', 'Sociology 👥'],
           "course": [1, 2, 3, 4],
           "goals": ['Dates 👫', 'Networking 🤝', 'Friendship 🤙']}

answers_val = ['/start', 'I am a Guy ‍👨‍💼', 'I am a Lady 👩‍💼', 'Kantemirovskaya 🏭', 'Griboedova 🏨', 'Promyshlennaya 🏫', 'Sedova 🏠', 'Logistics 🚚',
               'InterBusiness 💼', 'Economics 📈', 'InterBac 🤹‍', 'PMI 💻', 'Data Analytics 📊', 'Physics 🌌', 'Law ⚖️',
               'History 📜', 'Mediacommunications 📱', 'Philology 📚', 'Politology 🏛️', 'Vostokovedenie ⛩️', 'Design 🎨', 'UAGS 🏢', 'Sociology 👥',
               '1', '2', '3', '4', 'Dates 👫', 'Networking 🤝', 'Friendship 🤙']

# KEYBOARDS
kb_gender = [
        [types.KeyboardButton(text='I am a Guy ‍👨‍💼')],
        [types.KeyboardButton(text='I am a Lady ‍👩‍💼')],
        [types.KeyboardButton(text='Cancel ❌')]
    ]
keyboard_gender = types.ReplyKeyboardMarkup(keyboard=kb_gender,
                                            resize_keyboard=True,
                                            input_field_placeholder='Choose your gender'
                                            )

kb_campus = [
        [types.KeyboardButton(text='Kantemirovskaya 🏭')],
        [types.KeyboardButton(text='Griboedova 🏨')],
        [types.KeyboardButton(text='Promyshlennaya 🏫')],
        [types.KeyboardButton(text='Sedova 🏠')],
        [types.KeyboardButton(text='Cancel ❌')]
    ]
keyboard_campus = types.ReplyKeyboardMarkup(keyboard=kb_campus,
                                            resize_keyboard=True,
                                            input_field_placeholder='Choose your study campus'
                                            )

kb_kanta = [
            [types.KeyboardButton(text='Logistics 🚚')],
            [types.KeyboardButton(text='InterBusiness 💼')],
            [types.KeyboardButton(text='Economics 📈')],
            [types.KeyboardButton(text='InterBac 🤹‍')],
            [types.KeyboardButton(text='PMI 💻')],
            [types.KeyboardButton(text='Data Analytics 📊')],
            [types.KeyboardButton(text='Physics 🌌')],
            [types.KeyboardButton(text='Law ⚖️')],
            [types.KeyboardButton(text='Cancel ❌')]
        ]

kb_griba = [
            [types.KeyboardButton(text='History 📜')],
            [types.KeyboardButton(text='Mediacommunications 📱')],
            [types.KeyboardButton(text='Philology 📚')],
            [types.KeyboardButton(text='Politology 🏛️')],
            [types.KeyboardButton(text='Vostokovedenie ⛩️')],
            [types.KeyboardButton(text='Cancel ❌')]
        ]

kb_proma = [
            [types.KeyboardButton(text='Design 🎨')],
            [types.KeyboardButton(text='UAGS 🏢')],
            [types.KeyboardButton(text='Cancel ❌')]
        ]

course_kb = [
        [types.KeyboardButton(text='1 👶')],
        [types.KeyboardButton(text='2 🧒')],
        [types.KeyboardButton(text='3 🧔‍')],
        [types.KeyboardButton(text='4 👴')],
        [types.KeyboardButton(text='Cancel ❌')]
    ]

course_keyboard = types.ReplyKeyboardMarkup(keyboard=course_kb,
                                            resize_keyboard=True,
                                            input_field_placeholder='Choose your course'
                                            )

# COMMANDS


# universal command to cancel any action and return to /start
@router.message(Command('Cancel ❌'))
@router.message(F.text.casefold() == 'cancel ❌')
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.clear()
    await message.answer(
        '🫣Uh-oh! Cancelled the action and erased your ad.\n<b>Press /start again!</b>',
        reply_markup=ReplyKeyboardRemove(),
        # idea: we know state - so we just add keyboard that is relevant. and we clear only needed things
    )

'''
# if person tries to interrupt registration
@router.message(
    ~F.text.in_(answers_val),
    Form.unfinished
    )
async def not_finished(message: types.Message, state: FSMContext):
    await message.answer("Please let's postpone all conversations for later. You shall finish registering your ad!\n<b>Click on the buttons</b>👇")
'''


# start the bot and registration
@router.message(StateFilter(None), Command('start'))
async def gender_choice(message: types.Message, state: FSMContext) -> None:
    # setting first property - ID
    await state.set_state(Form.id)
    await state.update_data(id=message.from_user.id)
    await message.answer_photo('https://cutt.ly/cwTbybUB', 'Welcome to the world of Moura!🫰\n\n<b>STEP 1/6📝</b>\nTell us about yourself:',
                               reply_markup=keyboard_gender)
    await state.set_state(Form.gender)  # setting state that we chose gender

    # await message.answer('Welcome to the world of Moura. Tell us about yourself', reply_markup=keyboard)
    # await moura.send_message(config.admin_id.get_secret_value(), text='Moura is active')


@router.message(
    Form.gender,
    F.text.in_(['I am a Guy ‍👨‍💼', 'I am a Lady ‍👩‍💼'])
)
async def gender_chosen(message: types.Message, state: FSMContext) -> None:
    # setting gender
    await state.update_data(gender=1 if message.text == 'I am a Guy ‍👨‍💼' else 2)

    # Log updated data
    data = await state.get_data()
    sdata = ", ".join([f"{key} - {value}" for key, value in data.items()])
    logging.info("User data for id "+str(message.from_user.id)+" is set to "+sdata)

    gendr = 'bro' if message.text == 'I am a Guy ‍👨‍💼' else 'lady'
    await message.answer_photo('https://cutt.ly/xwTbFx6J',
                               f'Okay, {gendr}!\n\n<b>STEP 2/6📝</b>\nThen we determine your HSE campus. Choose one of yours below:👇',
                               reply_markup=keyboard_campus)
    await state.set_state(Form.campus)


@router.message(
    Form.campus,
    F.text.in_(['Kantemirovskaya 🏭', 'Griboedova 🏨', 'Promyshlennaya 🏫', 'Sedova 🏠'])
)
async def campus_chosen(message: types.Message, state: FSMContext):
    # setting campus
    await state.update_data(campus=message.text)

    # Log updated data
    data = await state.get_data()
    sdata = ", ".join([f"{key} - {value}" for key, value in data.items()])
    logging.info("User data for id " + str(message.from_user.id) + " is set to " + sdata)

    # process individual case with Sedova
    if message.text == 'Sedova 🏠':
        await state.update_data(campus=message.text)
        await state.set_state(Form.program)
        await state.update_data(program='Sociology 👥')
        await state.set_state(Form.course)
        await program_chosen(message, state)
        return

    keyboard_programs = types.ReplyKeyboardMarkup(keyboard=(kb_kanta if message.text == 'Kantemirovskaya 🏭'
                                                            else (kb_griba if message.text == 'Griboedova 🏨'
                                                                  else (kb_proma if message.text == 'Promyshlennaya 🏫'
                                                                        else None))),
                                                  resize_keyboard=True,
                                                  input_field_placeholder='Choose your program'
                                                  )
    await state.update_data(campus=message.text)
    # conditional sending photos of campuses
    await message.answer('Each building of HSE is unique.🫶\nWe in Moura like all the campuses no matter their location!\n\n<b>STEP 3/6📝</b>\nWhich program do you study at?👀', reply_markup=keyboard_programs)
    await state.set_state(Form.program)


@router.message(
    Form.program,
    F.text.in_(
        ['Logistics 🚚', 'InterBusiness 💼', 'Economics 📈', 'InterBac 🤹‍', 'PMI 💻', 'Data Analytics 📊', 'Physics 🌌', 'Law ⚖️', 'History 📜',
         'Mediacommunications 📱', 'Philology 📚', 'Politology 🏛️', 'Vostokovedenie ⛩️', 'Design 🎨', 'UAGS 🏢'])
)
async def program_chosen(message: types.Message, state: FSMContext) -> None:
    # setting program
    await state.update_data(program=message.text)

    # Log updated data
    data = await state.get_data()
    sdata = ", ".join([f"{key} - {value}" for key, value in data.items()])
    logging.info("User data for id " + str(message.from_user.id) + " is set to " + sdata)

    await state.update_data(program=message.text)
    await message.reply(
        f'So, you study {message.text if message.text != "Sedova 🏠" else "Sociology 👥, so skipping the 3rd step"}!\n\n<b>STEP 4/6📝</b>\nWhat is your course?',
        reply_markup=course_keyboard, parse_mode=ParseMode.HTML)
    await state.set_state(Form.course)


# BASIC INFO IS FILLED, NOW WE FILL THE GOALS

goals = ['Dates 👫', 'Networking 🤝', 'Friendship 🤙']
chosen_goals = []

goals_builder = InlineKeyboardBuilder()
for goal in goals:
    goals_builder.add(types.InlineKeyboardButton(text=goal, callback_data=goal))
goals_builder.add(types.InlineKeyboardButton(text='Save💾', callback_data='save'))
goals_builder.adjust(3, 1, repeat=True)


@router.message(
    Form.course,
    F.text.in_(['1 👶', '2 🧒', '3 🧔‍', '4 👴'])
)
async def course_chosen(message: types.Message, state: FSMContext) -> None:
    # setting course
    await state.update_data(course=message.text)

    # Log updated data
    data = await state.get_data()
    sdata = ", ".join([f"{key} - {value}" for key, value in data.items()])
    logging.info("User data for id " + str(message.from_user.id) + " is set to " + sdata)

    await message.answer("We saved your basic information! No worries about it",  reply_markup=ReplyKeyboardRemove())

    await message.answer("<b>STEP 5/6📝</b>\nWhat are your boundaries and goals?\nThey can be romantic, networking "
                         "(co-projects) or just friendship.\nBe open and honest.",
                         reply_markup=goals_builder.as_markup())


@dp.callback_query()
async def callbacks(call: types.CallbackQuery, state: FSMContext):
    if call.data in goals:
        if call.data in chosen_goals:
            chosen_goals.remove(call.data)
        else:
            chosen_goals.append(call.data)
        if chosen_goals:
            await moura.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>STEP 5/6📝</b>\nYour chosen goals: <b>" + ', '.join(chosen_goals) + "</b>\n They will affect which people you will see", reply_markup=goals_builder.as_markup())
        else:
            await moura.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="<b>STEP 5/6📝</b>\nWhat are your boundaries and goals?\nThey can be romantic, networking (co-projects) or just friendship.\nBe open and honest.",
                                          reply_markup=goals_builder.as_markup())
    elif call.data == 'save':
        # Save chosen_goals to database or do whatever you need with them
        if chosen_goals:
            await state.set_state(Form.goals)
            await state.update_data(goals=chosen_goals)
            await moura.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Your goals have been saved!\n\n<b>" + ', '.join(chosen_goals) + "</b>\n\nThis will help Moura to find more suitable people for you!")
            await moura.send_message(chat_id=call.message.chat.id, text='<b>STEP 6/6📝</b>\nFinally, create an ad!\n\nDescribe what you want or offer something...',
                                     reply_markup=types.ForceReply(input_field_placeholder='Describe what you want or offer something...'))
            await state.set_state(Form.ad_text)
        else:
            await moura.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="<b>Choose any goal first!</b>\n\n<b>STEP 5/6📝</b>\nWhat are your boundaries and goals?\nThey can be romantic, networking (co-projects) or just friendship.\nBe open and honest.",
                                          reply_markup=goals_builder.as_markup())


# Finished
@router.message(
    Form.ad_text,
    F.text.len() > 10
)
async def finish(message: types.Message, state: FSMContext):
    await state.update_data(ad_text=message.text)
    data = await state.get_data()
    await message.answer(
        text=f"Your ad:\n{data}",
        reply_markup=ReplyKeyboardRemove()
    )
    # save it to database
    await state.clear()


# Not Finished
@router.message(
    Form.ad_text,
    F.text.len() <= 10
)
async def not_finished(message: types.Message, state: FSMContext):
    await message.reply('Your ad is too short. Try something again!')


async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True):
    text = 'You are ' + data.get('gender') + 'studying at ' + data.get('campus') + ' on ' + data.get(
        'program') + ' at ' + data.get('course') + ' course.\nYour ad:\n' + data.get('ad_text')
    await message.reply(text=text, reply_markup=ReplyKeyboardRemove())


# f'{message.html_text}'


async def main():
    await dp.start_polling(moura)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")








'''
             'interests': {
                 'Business💸': False,
                 'Finances📈': False,
                 'Oratory🎙️': False,
                 'Marketing📱': False,
                 'UX/UI🤳': False,
                 'Arts🎨': False,
                 'Acting🎭': False,
                 'Photography📸': False,
                 'Cinema🎥': False,
                 'Dancing💃': False,
                 'Music🎧': False,
                 'Sports & Health💪': False,
                 'Travelling🏕️': False,
                 'Fiction📚': False,
                 'Series👓': False,
                 'Programming👨‍💻': False,
                 'Sciences🔬': False,
                 'Stand-ups🎤': False,
                 'Artsy lifestyle🖼️': False,
                 'Parties🪩': False,
                 'Board Games🎲': False,
                 'Animals🐾': False,
             },'''
