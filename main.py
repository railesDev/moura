from aiogram.utils.keyboard import InlineKeyboardBuilder
from config_reader import config
import sys
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram import Router, F
from aiogram.filters import Command
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
             (id INTEGER PRIMARY KEY, gender integer, campus text, program text, course integer, goals integer, gender_goals integer, photo_id integer, ad_text text)''')

c.execute('''CREATE TABLE IF NOT EXISTS matches
             (id INTEGER PRIMARY KEY, match_id integer, reaction integer)''')
conn.commit()

# reactions: -1 not seen, 0 dislike, 1 like, 2 match

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
    gender_goals = State()
    photo_id = State()
    ad_text = State()
    finished = State()


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

gendergoals_kb = [
        [types.KeyboardButton(text='Guys 👨')],
        [types.KeyboardButton(text='Ladies ‍👩')],
        [types.KeyboardButton(text='Both 🤷')],
        [types.KeyboardButton(text='Cancel ❌')]
    ]

gendergoals_keyboard = types.ReplyKeyboardMarkup(keyboard=gendergoals_kb,
                                                 resize_keyboard=True,
                                                 input_field_placeholder='Choose your preferences'
                                                 )

photo_kb = [
        [types.KeyboardButton(text='No photo ❌')]
    ]

photo_keyboard = types.ReplyKeyboardMarkup(keyboard=photo_kb,
                                           resize_keyboard=True,
                                           input_field_placeholder='Upload photo or refuse'
                                           )

last_kb = [
        [types.KeyboardButton(text='Publish 🏹!')],
        [types.KeyboardButton(text='Start over 🔄')],
    ]

last_keyboard = types.ReplyKeyboardMarkup(keyboard=last_kb,
                                          resize_keyboard=True,
                                          input_field_placeholder='Finally, your decision...'
                                          )

awaiting_kb = [
        [types.KeyboardButton(text='Look at ads!')],
    ]

awaiting_keyboard = types.ReplyKeyboardMarkup(keyboard=awaiting_kb,
                                              resize_keyboard=True,
                                              input_field_placeholder="Let's go!!!"
                                              )

tinder_kb = [
    [types.KeyboardButton(text='Like 💟'),
     types.KeyboardButton(text='Next ⏩️')],
    [types.KeyboardButton(text='Complain ‼️')],
    ]

tinder_keyboard = types.ReplyKeyboardMarkup(keyboard=tinder_kb,
                                           resize_keyboard=True,
                                           input_field_placeholder='What do you think?'
                                           )

see_likes_kb = [
    [types.KeyboardButton(text='Look at my likes!💟')]
    ]

see_likes_keyboard = types.ReplyKeyboardMarkup(keyboard=see_likes_kb,
                                           resize_keyboard=True,
                                           input_field_placeholder='Wanna look?'
                                           )


likes_kb = [
    [types.KeyboardButton(text='Match 💟'),
     types.KeyboardButton(text='No 🚫')],
    [types.KeyboardButton(text='Complain ‼️')],
    ]

likes_keyboard = types.ReplyKeyboardMarkup(keyboard=likes_kb,
                                           resize_keyboard=True,
                                           input_field_placeholder='What do you think?'
                                           )

# COMMANDS

'''
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

# if person tries to interrupt registration
@router.message(
    ~F.text.in_(answers_val),
    Form.unfinished
    )
async def not_finished(message: types.Message, state: FSMContext):
    await message.answer("Please let's postpone all conversations for later. You shall finish registering your ad!\n<b>Click on the buttons</b>👇")
'''


# start the bot and registration
@router.message((F.text == '/start') | (F.text == 'Start over 🔄') | (F.text == 'Cancel ❌'))
async def gender_choice(message: types.Message, state: FSMContext) -> None:
    # setting first property - ID
    await state.clear()
    # if the user cleared history and tried to launch the /start again:
    id_to_check = message.from_user.id
    # Check if the ID exists in the table
    c.execute('''SELECT * FROM users WHERE id = ?''', (id_to_check,))
    # Fetch the result
    result = c.fetchone()
    # Check if the ID exists
    if result is not None or message.text == 'Cancel ❌':
        await message.answer(("Okay, let's restart filling your profile!🔮" if message.text == 'Cancel ❌' else "🧞Our digital minds say that you have been in Moura recently.\nWe delete your data from us and you shall start over!🔮"))
        c.execute('''DELETE FROM users WHERE id = ?''', (id_to_check,))
        c.execute('''DELETE FROM matches WHERE id = ?''', (id_to_check,))
        c.execute('''DELETE FROM matches WHERE match_id = ?''', (id_to_check,))
        conn.commit()

    await state.set_state(Form.id)
    await state.update_data(id=message.from_user.id)
    await message.answer_photo('https://cutt.ly/cwTbybUB', 'Welcome to the world of Moura!🫰\n\n<b>STEP 1/8📝</b>\nTell us about yourself:',
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
    await message.answer_photo('https://cutt.ly/hwTVzUO7',
                               f'Okay, {gendr}!\n\n<b>STEP 2/8📝</b>\nThen we determine your HSE campus. Choose one of yours below:👇',
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

    await moura.send_animation(message.from_user.id, ('https://cutt.ly/TwTVUdvU' if message.text == 'Kantemirovskaya 🏭'
                                                      else ('https://cutt.ly/4wTVUUdQ' if message.text == 'Griboedova 🏨'
                                                            else ('https://cutt.ly/OwTVHoIR' if message.text == 'Promyshlennaya 🏫'
                                                                  else ('https://cutt.ly/swTVIkDr' if message.text == 'Sedova 🏠' else None)))),
                               caption='Each building of HSE is unique.🫶\nWe in Moura like all the campuses no matter their location!')

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

    await message.answer('<b>STEP 3/8📝</b>\nWhich program do you study at?👀', reply_markup=keyboard_programs)
    await state.set_state(Form.program)


@router.message(
    Form.program,
    F.text.in_(
        ['Logistics 🚚', 'InterBusiness 💼', 'Economics 📈', 'InterBac 🤹‍', 'PMI 💻', 'Data Analytics 📊', 'Physics 🌌', 'Law ⚖️', 'History 📜',
         'Mediacommunications 📱', 'Philology 📚', 'Politology 🏛️', 'Vostokovedenie ⛩️', 'Design 🎨', 'UAGS 🏢'])
)
async def program_chosen(message: types.Message, state: FSMContext) -> None:
    # setting program
    data = await state.get_data()
    try:
        prog = data["program"]
    except KeyError:
        await state.update_data(program=message.text)
    # Log updated data
    data = await state.get_data()
    sdata = ", ".join([f"{key} - {value}" for key, value in data.items()])
    logging.info("User data for id " + str(message.from_user.id) + " is set to " + sdata)

    await state.update_data(program=message.text)
    await message.reply(
        f'So, you study <b>{message.text if message.text != "Sedova 🏠" else "Sociology 👥, so skipping the 3rd step"}!</b>\n\n<b>STEP 4/8📝</b>\nWhat is your course?',
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

    await message.answer("Sooo, we are done with your basic information!\n<b>Let's go for a next step!😎</b>",
                         reply_markup=ReplyKeyboardRemove())

    await message.answer("<b>STEP 5/8📝</b>\nWhat are your boundaries and goals?\nThey can be romantic, networking "
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
            await moura.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>STEP 5/8📝</b>\nYour chosen goals: <b>" + ', '.join(chosen_goals) + "</b>\nThey will affect which people you will see", reply_markup=goals_builder.as_markup())
        else:
            await moura.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="<b>STEP 5/8📝</b>\nWhat are your boundaries and goals?\nThey can be romantic, networking (co-projects) or just friendship.\nBe open and honest.",
                                          reply_markup=goals_builder.as_markup())
    elif call.data == 'save':
        # Save chosen_goals to database or do whatever you need with them
        if chosen_goals:
            await state.set_state(Form.goals)
            await state.update_data(goals=chosen_goals)
            await moura.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Your goals have been saved!\n\n<b>" + ', '.join(chosen_goals) + "</b>\n\nThis will help Moura to find more suitable people for you!")
            await state.set_state(Form.gender_goals)
            await moura.send_message(chat_id=call.message.chat.id,
                                     text="<b>STEP 6/8📝</b>\nWhat about your gender preferences? Who should Moura show you?",
                                     reply_markup=gendergoals_keyboard)
        else:
            await moura.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="<b>Choose any goal first!</b>\n\n<b>STEP 5/8📝</b>\nWhat are your boundaries and goals?\nThey can be romantic, networking (co-projects) or just friendship.\nBe open and honest.",
                                          reply_markup=goals_builder.as_markup())


# 2 - both, 1 - i want girls, 0 - i want boys
# dating = full correlation
# others - any
'''
Protection from homophobia
IF GENDER = MALE, GENDER PREFERENCE = 2 AND NOT ONLY DATING, BUT DATING IS SET, INCOMING_AD.PREFERENCE==1 AND GENDER == 1 - miss
'''


@router.message(
   Form.gender_goals
)
async def gendergoals_set(message: types.Message, state: FSMContext) -> None:
    await state.update_data(gender_goals=(2 if message.text == 'Both 🤷'
                                          else (1 if message.text == 'Ladies ‍👩'
                                                else (0 if message.text == 'Guys 👨' else -1))))
    await state.set_state(Form.photo_id)
    await message.answer("<b>STEP 7/8📝</b>\nNow, if you wish, you can attach a photo to your ad! It will increase your chance to match!",
                         reply_markup=photo_keyboard)


@router.message(
   Form.photo_id
)
async def photo_sent(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.ad_text)
    try:
        if message.text == 'No photo ❌':
            await state.update_data(photo_id='AgACAgIAAxkBAAIGJmVNcnV831dIx07HTQQayc5tk8bnAAI01DEb0oFxSvQ-2w8nblOoAQADAgADeQADMwQ')
    except Exception:
        pass
    try:
        await state.update_data(photo_id=message.photo[-1].file_id)
    except Exception:
        pass
    await state.set_state(Form.ad_text)
    await message.answer('As we are done with photos,...\n\n<b>STEP 8/8📝</b>\nFinally, create a description!\nThis is the most important part in your ad.\n\nDescribe what you want or offer something...',
                         reply_markup=types.ForceReply(
                             input_field_placeholder='Describe what you want or offer something...'))


def parse_ad(data):
    sdata = ""
    photoid = ""
    logging.info("DATA to parse ad: "+str(data))
    for key, value in data.items():
        if key not in ["id", "ad_text", "goals", "photo_id", "gender_goals"]:
            sdata += "<b>"+key[0].upper()+key[1:]+":</b> "+(value if key != "gender" else "male" if value == 1 else "female")+"\n\n"
        else:
            if key == "ad_text":
                sdata = "<b>Ad text:</b> "+value+"\n\n" + sdata
            if key == "goals":
                sdata += "<b>"+key[0].upper()+key[1:]+":</b> "+', '.join(value)+"\n\n"
            if key == "gender_goals":
                sdata += "<b>Your preferences:</b> " + ('Ladies ‍👩' if value == 1
                                                                    else ('Both 🤷' if value == 2
                                                                          else ('Guys 👨' if value == 0
                                                                                else None))) + "\n\n"
            if key == "photo_id":
                photoid = value
    return sdata, photoid


# 111 - Dates, Networking, Friendship
def goals_encoder(goals_data, decode=False):
    if decode:
        output = ""
        if goals_data // 100 != 0:
            output += 'Dates 👫, '
        if goals_data % 100 // 10 != 0:
            output += 'Networking 🤝, '
        if goals_data % 10 != 0:
            output += 'Friendship 🤙'
        return output
    else:
        code = 0
        for g in goals_data:
            if g == 'Dates 👫':
                code += 100
            if g == 'Networking 🤝':
                code += 10
            if g == 'Friendship 🤙':
                code += 1
        return code


# Finishing
@router.message(
    Form.ad_text,
    F.text.len() > 10
)
async def register_finishing(message: types.Message, state: FSMContext):
    await state.update_data(ad_text=message.text)
    data = await state.get_data()
    sdata = parse_ad(data)
    await message.answer_photo(sdata[1],
                               caption=f"<b>WE ARE ALL DONE!✅\nLook at your ad:</b>\n\n{sdata[0]}\n\nIs everything correct? <b>If yes, click Publish!</b>",
                               reply_markup=last_keyboard
                               )
    await state.set_state(Form.finished)


# Not Finishing
@router.message(
    Form.ad_text,
    F.text.len() <= 10
)
async def not_finished(message: types.Message, state: FSMContext):
    await message.reply('Your ad is too short. Try something again!👇')


class Matches(StatesGroup):
    awaiting = State()
    action = State()
    matched = State()


# FIND MATCHES and ADD TO EXISTING
def find_matches(user_id):
    c.execute('''
        SELECT id, gender, gender_goals, goals
        FROM users
        WHERE id = ?
    ''', (user_id,))
    user_data = c.fetchone()
    # 2 - ggoals, 1 - gender, 3 - goals

    # find everyone suitable
    c.execute('''
        SELECT id
        FROM users
        WHERE (id != ?) AND (gender = ? OR gender = ?) AND (gender_goals = ? OR gender_goals = ?) AND (((goals + ?) / 100 = 2) OR ((goals + ?) % 100 / 10 = 2) OR ((goals + ?) % 10 = 2))
    ''', (user_data[0], (2 if user_data[2] == 1 else (1 if user_data[2] == 0 else 1)), (2 if user_data[2] == 1 else (1 if user_data[2] == 0 else 2)), (0 if user_data[1] == 1 else (1 if user_data[1] == 2 else None)), 2, user_data[3], user_data[3], user_data[3]))

    matches = c.fetchall()

    for match in matches:
        c.execute('''
            INSERT OR IGNORE INTO matches (id, match_id, reaction)
            VALUES (?, ?, ?)
        ''', (user_id, match[0], -1))
        c.execute('''
            INSERT OR IGNORE INTO matches (id, match_id, reaction)
            VALUES (?, ?, ?)
            ''', (match[0], user_id, -1))

    conn.commit()


def get_match_data(match_id):

    c.execute('''
        SELECT *
        FROM users
        WHERE id = ?
    ''', (match_id,))

    match_data = c.fetchone()

    return match_data


# 111 - Dates, Networking, Friendship
def unpack_ad(data):
    return (("Guy, " if data[1] == 1 else ", ")+"MouraID: "+str(data[0])+"\nStudies at "+data[2]+" on "+data[3] +
            ", course - "+data[4][0]+"\nSearches for: "+("dates, " if data[5] // 100 != 0 else "") +
            ("networking, " if data[5] % 100 // 10 != 0 else "") +
            ("friendship" if data[5] % 10 != 0 else "")+"\n\n"+data[8])


# Finished
@router.message(
    Form.finished,
    F.text == 'Publish 🏹!'
)
async def register_finishing(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sdata = list(data.values())
    sdata[5] = goals_encoder(sdata[5])
    await message.answer(
        text=f"<b>Your ad is published!🤩</b>\n Now let's start matching!",
        reply_markup=awaiting_keyboard
    )
    # Insert the user data into the table
    c.execute('''INSERT INTO users (id, gender, campus, program, course, goals, gender_goals, photo_id, ad_text) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', sdata)

    # Commit the transaction
    conn.commit()
    # save it to database
    await state.clear()
    find_matches(message.from_user.id)
    conn.commit()

    await state.set_state(Matches.awaiting)


@router.message(
    Matches.awaiting
)
async def get_new_ad(message: types.Message, state: FSMContext):
    while True:
        c.execute('''
                    SELECT match_id
                    FROM matches
                    WHERE id = ? AND reaction = ?
                ''', (message.from_user.id, -1))

        match_id = c.fetchone()
        if match_id is not None:
            match_data = get_match_data(match_id[0])
            await message.answer_photo(str(match_data[7]), unpack_ad(match_data), reply_markup=tinder_keyboard)
            await state.set_state(Matches.action)
            await state.update_data(awaiting=match_id[0])
            break
        else:
            data = await state.get_data()
            try:
                if data["awaiting"] != 0:
                    await message.answer("For now no more ads. Wait for them!")
                    await state.update_data(awaiting=0)
            except KeyError:
                await message.answer("For now no more ads. Wait for them!")
                await state.update_data(awaiting=0)
            await asyncio.sleep(1)  # wait for 1 second before checking again


@router.message(
    Matches.action
)
async def perform_action(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'Like 💟':
        c.execute(f'''
                UPDATE matches
                SET reaction = ?
                WHERE reaction != 2 AND id = ?
            ''', (1, data["awaiting"]))
        c.execute(f'''
                UPDATE matches
                SET reaction = ?
                WHERE reaction != 2 AND match_id = ?
            ''', (1, data["awaiting"]))
        conn.commit()
        await moura.send_message(chat_id=data["awaiting"], text="You have a new like!", reply_markup=see_likes_keyboard)
        await message.answer("Like was sent!", reply_markup=awaiting_keyboard)
        await state.set_state(Matches.awaiting)

    elif message.text == 'Next ⏩️':
        c.execute(f'''
                        UPDATE matches
                        SET reaction = ?
                        WHERE reaction != 2 AND id = ?
                    ''', (0, data["awaiting"]))
        c.execute(f'''
                        UPDATE matches
                        SET reaction = ?
                        WHERE reaction != 2 AND match_id = ?
                        ''', (0, data["awaiting"]))
        conn.commit()
        await message.answer("Okay, next one?",
                             reply_markup=awaiting_keyboard)
        await state.set_state(Matches.awaiting)
    elif message.text == 'Complain ‼️':
        c.execute(f'''
                        UPDATE matches
                        SET reaction = ?
                        WHERE reaction != 2 AND id = ?
                        ''', (0, data["awaiting"]))
        c.execute(f'''
                        UPDATE matches
                        SET reaction = ?
                        WHERE reaction != 2 AND match_id = ?
                        ''', (0, data["awaiting"]))
        conn.commit()
        await message.answer("Please forward this ad to @heliumwer, he will deal with this person!", reply_markup=awaiting_keyboard)
        await state.set_state(Matches.awaiting)


@dp.message(F.text == "Look at my likes!💟")
async def look_at_new_like(message: types.Message, state: FSMContext):
    c.execute('''
            SELECT match_id
            FROM matches
            WHERE id = ? AND reaction = 1
            ''', (message.from_user.id,))
    match_id = c.fetchone()[0]
    c.execute('''
            SELECT *
            FROM users
            WHERE id = ?
        ''', (match_id,))
    match_data = c.fetchone()
    await state.update_data(awaiting=match_id)
    await message.answer_photo(str(match_data[7]), unpack_ad(match_data), reply_markup=likes_keyboard)


@dp.message(F.text == "Match 💟")
async def match(message: types.Message, state: FSMContext):
    data = await state.get_data()
    c.execute(f'''
                    UPDATE matches
                    SET reaction = ?
                    WHERE reaction != 2 AND id = ?
                ''', (2, data["awaiting"]))
    c.execute(f'''
                    UPDATE matches
                    SET reaction = ?
                    WHERE reaction != 2 AND match_id = ?
                ''', (2, data["awaiting"]))
    conn.commit()
    # later here will be some actions - choose context, choose place.
    logging.info(str(int(data['awaiting'])))
    await message.answer(f"Write to [your new match\!](tg://user?id={int(data['awaiting'])})", parse_mode=ParseMode.MARKDOWN_V2, reply_markup=awaiting_keyboard)
    await state.set_state(Matches.awaiting)
    # to the one with whom we matched, will happen nothing. everything is on our initiative.


@dp.message(F.text == "No 🚫")
async def match(message: types.Message, state: FSMContext):
    data = await state.get_data()
    c.execute(f'''
                    UPDATE matches
                    SET reaction = ?
                    WHERE reaction != 2 AND id = ?
                ''', (0, data["awaiting"]))
    c.execute(f'''
                    UPDATE matches
                    SET reaction = ?
                    WHERE reaction != 2 AND match_id = ?
                ''', (0, data["awaiting"]))
    conn.commit()
    await message.answer("Okay, next one?",
                         reply_markup=awaiting_keyboard)
    await state.set_state(Matches.awaiting)


@dp.message(F.text == 'Complain ‼️')
async def complain(message: types.Message, state: FSMContext):
    data = await state.get_data()
    c.execute(f'''
        UPDATE matches
        SET reaction = ?
        WHERE reaction != 2 AND id = ?
        ''', (0, data["awaiting"]))
    c.execute(f'''
        UPDATE matches
        SET reaction = ?
        WHERE reaction != 2 AND match_id = ?
        ''', (0, data["awaiting"]))
    conn.commit()
    await message.answer("Please forward this ad to @heliumwer, he will deal with this person!", reply_markup=awaiting_keyboard)
    await state.set_state(Matches.awaiting)
















async def main():
    await dp.start_polling(moura)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")








'''
ADD THEM IN THE FUTURE
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
