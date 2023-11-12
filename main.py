from aiogram.utils.keyboard import InlineKeyboardBuilder
from config_reader import config
import sys
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums import ParseMode
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
import sqlite3
import keyboards

logging.basicConfig(level=logging.INFO)

female_anon_photo_id = 'AgACAgIAAxkBAAIGJmVNcnV831dIx07HTQQayc5tk8bnAAI01DEb0oFxSvQ-2w8nblOoAQADAgADeQADMwQ'
male_anon_photo_id = 'AgACAgIAAxkBAAIQxGVQA6sCMjjYnNgsUaCdusBZB4xyAAITzjEb7JSASjy2e7xU6PkMAQADAgADeQADMwQ'

# Connect to the SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()


# Create the users table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, gender integer, campus text, program text, course integer, frd_goal integer, dts_goal integer, ntw_goal integer, gender_goals integer, photo_id integer, ad_text text)''')

c.execute('''CREATE TABLE IF NOT EXISTS reactions
             (id INTEGER PRIMARY KEY, match_id integer, reaction integer)''')
conn.commit()


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


# COMMANDS

# start the bot and registration
@router.message((F.text == '/start') | (F.text == 'Start over 🔄') | (F.text == '🔮Return to Moura!🔮'))
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
    if result is not None or message.text == 'Start over 🔄':
        await message.answer(("Okay, let's restart filling your profile!🔮" if message.text == 'Start over 🔄' else "🧞Our digital minds say that you have been in Moura recently.\nWe deleted your data from us and you shall start over!🔮"))
        c.execute('''DELETE FROM users WHERE id = ?''', (id_to_check,))
        c.execute('''DELETE FROM reactions WHERE id = ?''', (id_to_check,))
        c.execute('''DELETE FROM reactions WHERE match_id = ?''', (id_to_check,))
        conn.commit()
        await gender_choice(message, state)
    else:
        await message.answer_photo('https://cutt.ly/LwYgpImT',
                                   '<b>Hey!👋 Announcements channel: @mourahse</b>\n\nBot is inactive until you enter the access code:\n<i>*hint: you can find it in the posters and ads</i>',
                                   reply_markup=ReplyKeyboardRemove())


@router.message((F.text.upper() == 'HSEMR'))
async def gender_choice(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.id)
    await state.update_data(id=message.from_user.id)
    await message.answer_photo('https://cutt.ly/cwTbybUB', 'Welcome to the world of Moura!🫰\n\n<b>STEP 1/8📝</b>\nTell us about yourself:',
                               reply_markup=keyboards.keyboard_gender)
    await state.set_state(Form.gender)  # setting state that we chose gender


@router.message(
    Form.gender,
    F.text.in_(['I am a Guy ‍👨‍💼', 'I am a Lady ‍👩‍💼'])
)
async def gender_chosen(message: types.Message, state: FSMContext) -> None:
    # setting gender
    await state.update_data(gender=1 if message.text == 'I am a Guy ‍👨‍💼' else 0)

    # Log updated data
    data = await state.get_data()
    sdata = ", ".join([f"{key} - {value}" for key, value in data.items()])
    logging.info("User data for id "+str(message.from_user.id)+" is set to "+sdata)
    # https://cutt.ly/hwTVzUO7

    gendr = 'bro' if message.text == 'I am a Guy ‍👨‍💼' else 'lady'
    await message.answer_photo('https://cutt.ly/3wYopqmz',
                               f'Okay, {gendr}!\n\n<b>STEP 2/8📝</b>\nThen we determine your HSE campus. Choose one of yours below:👇',
                               reply_markup=keyboards.keyboard_campus)
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

    await message.answer_photo(('https://cutt.ly/awYogHta' if message.text == 'Kantemirovskaya 🏭'
                                else ('https://cutt.ly/MwYogMg4' if message.text == 'Griboedova 🏨'
                                      else ('https://cutt.ly/CwYog9ZH' if message.text == 'Promyshlennaya 🏫'
                                            else ('https://cutt.ly/0wYog5yQ' if message.text == 'Sedova 🏠' else None))
                                      )),
                               caption='Each building of HSE is unique🫶\n'
                                       'We in Moura admire all the campuses and their students!')

    # process individual case with Sedova
    if message.text == 'Sedova 🏠':
        await state.update_data(campus=message.text)
        await state.set_state(Form.program)
        await state.update_data(program='Sociology 👥')
        await state.set_state(Form.course)
        await program_chosen(message, state)
        return

    keyboard_programs = types.ReplyKeyboardMarkup(keyboard=
                                                  (keyboards.kb_kanta if message.text == 'Kantemirovskaya 🏭'
                                                   else (keyboards.kb_griba if message.text == 'Griboedova 🏨'
                                                         else (keyboards.kb_proma if message.text == 'Promyshlennaya 🏫'
                                                               else None))),
                                                  resize_keyboard=True,
                                                  input_field_placeholder='Choose your program'
                                                  )
    await state.update_data(campus=message.text)
    # https://cutt.ly/xwYohUV6

    await message.answer_photo('https://cutt.ly/owYoxOJt',
                               '<b>STEP 3/8📝</b>\nWhich program do you study at?👀',
                               reply_markup=keyboard_programs)
    await state.set_state(Form.program)


@router.message(
    Form.program,
    F.text.in_(
        ['Logistics 🚚', 'InterBusiness 💼', 'Economics 📈', 'InterBac 🤹‍', 'PMI 💻', 'Data Analytics 📊', 'Physics 🌌',
         'Law ⚖️', 'History 📜', 'Mediacommunications 📱', 'Philology 📚', 'Politology 🏛️', 'Vostokovedenie ⛩️',
         'Design 🎨', 'UAGS 🏢'])
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
    # https://cutt.ly/UwYohMKf
    await message.reply_photo('https://cutt.ly/bwYoxLwG',
                              f'So, you study <b>{message.text if message.text != "Sedova 🏠" else "Sociology 👥, so skipping the 3rd step"}!</b>\n\n<b>STEP 4/8📝</b>\nWhat is your course?',
                              reply_markup=keyboards.course_keyboard,
                              parse_mode=ParseMode.HTML)
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
    # https://cutt.ly/RwYojeCp

    await message.answer_photo('https://cutt.ly/HwYox0Yv',
                               "So, we are done with your basic information!\n<b>Let's go for a next step!😎</b>",
                               reply_markup=ReplyKeyboardRemove())

    await message.answer("<b>STEP 5/8📝</b>\nWhat are your boundaries and goals?\n\nAre you into dates, networking "
                         "(co-projects) or just friendship?",
                         reply_markup=goals_builder.as_markup())


@dp.callback_query()
async def callbacks(call: types.CallbackQuery, state: FSMContext):
    if call.data in goals:
        if call.data in chosen_goals:
            chosen_goals.remove(call.data)
        else:
            chosen_goals.append(call.data)
        if chosen_goals:
            with suppress(TelegramBadRequest):
                await moura.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>STEP 5/8📝</b>\nYour chosen goals:\n<b>" + ', '.join(chosen_goals) + "</b>\n\nThey will affect which people you will see\n<b>Don't forget to click Save💾!</b>\n\n<i>*to cancel selection, click on a button again</i>", reply_markup=goals_builder.as_markup())
        else:
            with suppress(TelegramBadRequest):
                await moura.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="<b>STEP 5/8📝</b>\nWhat are your boundaries and goals?\n\n"
                                                   "Are you into dates, networking (co-projects) or just friendship?",
                                              reply_markup=goals_builder.as_markup())
    elif call.data == 'save':
        if chosen_goals:
            await state.set_state(Form.goals)
            await state.update_data(goals=chosen_goals)
            with suppress(TelegramBadRequest):
                await moura.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>STEP 5/8📝</b>\nYour goals have been saved!\n\n<b>" + ', '.join(chosen_goals) + "</b>\n\nThis will help Moura to find more suitable people for you!")
            await state.set_state(Form.gender_goals)
            # https://cutt.ly/twYojDyB
            await moura.send_photo(chat_id=call.message.chat.id,
                                   photo='https://cutt.ly/NwYocqmG',
                                   caption="<b>STEP 6/8📝</b>\nWhat about your gender preferences? Who should Moura show you?",
                                   reply_markup=keyboards.gendergoals_keyboard)
        else:
            with suppress(TelegramBadRequest):
                await moura.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="<b>Choose any goal first!</b>\n\n<b>STEP 5/8📝</b>\nWhat are your boundaries and goals?\nYour choice will affect which people you will see",
                                              reply_markup=goals_builder.as_markup())



'''
Protection from homophobia
IF GENDER = MALE, GENDER PREFERENCE = 2 AND NOT ONLY DATING, BUT DATING IS SET, INCOMING_AD.PREFERENCE==1 AND GENDER == 1 - miss
'''


@router.message(
   Form.gender_goals
)
async def gendergoals_set(message: types.Message, state: FSMContext) -> None:
    await state.update_data(gender_goals=(2 if message.text == 'Both 🤷'
                                          else (0 if message.text == 'Ladies ‍👩'
                                                else (1 if message.text == 'Guys 👨' else -1))))
    await state.set_state(Form.photo_id)
    # https://cutt.ly/mwYojXB7
    await message.answer_photo('https://cutt.ly/BwYocaLZ',
                               "<b>STEP 7/8📝</b>\nNow, if you wish, you can attach a photo to your ad! It will increase your chance to match!",
                               reply_markup=keyboards.photo_keyboard)


@router.message(
   Form.photo_id, (F.photo | F.text == 'No photo ❌')
)
async def photo_sent(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.ad_text)
    try:
        if message.text == 'No photo ❌':
            data = await state.get_data()
            await state.update_data(photo_id=(female_anon_photo_id if data["gender"] == 0 else male_anon_photo_id))
    except Exception:
        pass
    try:
        await state.update_data(photo_id=message.photo[-1].file_id)
    except Exception:
        pass
    await state.set_state(Form.ad_text)
    # https://cutt.ly/twYoj49Y
    await message.answer_photo('https://cutt.ly/LwYoclfw',
                               'As we are done with photos,...\n\n<b>STEP 8/8📝</b>\nFinally, create a description!\nThis is the most important part in your ad.\n\n<b>Describe your desires or offer something</b>',
                               reply_markup=types.ForceReply(
                                   input_field_placeholder='See it as your Twitter'))


def parse_ad(data):
    sdata = ""
    photoid = ""
    logging.info("DATA to parse ad: "+str(data))
    for key, value in data.items():
        if key not in ["id", "ad_text", "goals", "photo_id", "gender_goals"]:
            sdata += "<b>"+key[0].upper()+key[1:]+":</b> "+(value if key != "gender" else "male" if value == 1 else "female")+"\n"
        else:
            if key == "ad_text":
                sdata = "<b>Description:</b>\n"+value+"\n\n\n" + sdata
            if key == "goals":
                sdata += "<b>"+key[0].upper()+key[1:]+":</b> "+', '.join(value)+"\n"
            if key == "gender_goals":
                sdata += "<b>Preferences:</b> " + ('Ladies ‍👩' if value == 0
                                                                    else ('Both 🤷' if value == 2
                                                                          else ('Guys 👨' if value == 1
                                                                                else None))) + "\n"
            if key == "photo_id":
                photoid = value
    return sdata, photoid


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
                               caption=f"<b>✅ WE ARE ALL DONE! Look at your ad:</b>\n\n{sdata[0]}\nIs everything correct? <b>If yes, click Publish!</b>",
                               reply_markup=keyboards.last_keyboard
                               )
    await state.set_state(Form.finished)


# Ad is too short
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


def get_match_data(match_id):
    c.execute('''
        SELECT *
        FROM users
        WHERE id = ?
    ''', (match_id,))
    match_data = c.fetchone()
    return match_data


def unpack_ad(data):
    return (data[8]+"\n\n"+("Guy, " if data[1] == 1 else "Lady, ")+"MouraID: "+str(data[0])+"\nStudies at "+data[2] +
            " on "+data[3] + ", course - "+data[4][0]+"\nSearches for: "+("dates, " if data[5][1] else "") +
            ("networking, " if data[5][2] else "")+("friendship" if data[5][0] else ""))


def goals_encoder(goals_data, decode=False):
    if decode:
        output = goals_data[0]*'Friendship 🤙, '+goals_data[1]*'Dates 👫, '+goals_data[2]*'Networking 🤝'
        return output
    else:
        code = ['Friendship 🤙' in goals_data, 'Dates 👫' in goals_data, 'Networking 🤝' in goals_data]
        return code


# Finished
@router.message(
    Form.finished,
    F.text == 'Publish 🏹!'
)
async def register_finishing(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sdata = list(data.values())
    sdata[5] = goals_encoder(sdata[5])
    sdata = sdata[:5] + [sdata[5][0], sdata[5][1], sdata[5][2]] + sdata[6:]
    await message.answer(
        text=f"<b>Your ad is published!🤩</b>\nNow let's start matching!",
        reply_markup=keyboards.awaiting_keyboard
    )
    # Insert the user data into the table
    c.execute('''INSERT INTO users (id, gender, campus, program, course, frd_goal, dts_goal, 
    ntw_goal, gender_goals, photo_id, ad_text) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', sdata)
    # Commit the transaction
    conn.commit()
    # save it to database
    await state.clear()
    conn.commit()
    await state.set_state(Matches.awaiting)


@router.message(
    Matches.awaiting,
    F.text == '🔮Show me an ad!🔮'
)
async def get_new_ad(message: types.Message, state: FSMContext):
    logging.info("WARNING: WARNING: WARNING: Started searching for matches\n\n\n")
    while True:
        # extract our current user info
        c.execute('''
            SELECT id, gender, gender_goals, frd_goal, dts_goal, ntw_goal
            FROM users
            WHERE id = ?
            LIMIT 1
        ''', (message.from_user.id,))
        user_data = c.fetchone()
        logging.info("USER DATA: "+str(user_data)+"\n\n\n")
        # try to find a match for him if any left
        c.execute('''
                    SELECT users.id
                    FROM users
                    JOIN reactions ON users.id = reactions.id
                    WHERE reactions.reaction != 0 
                    AND (
                    (users.gender_goals = ? OR users.gender_goals = 2) AND (users.gender = ? OR ? = 2) AND (users.frd_goal*? = 1 OR users.dts_goal*? = 1 OR users.ntw_goal*? = 1)
                    )
                    AND users.id NOT IN (SELECT reactions.match_id FROM reactions WHERE reactions.id = users.id) 
                    LIMIT 1
                ''', (user_data[1], user_data[2], user_data[2], user_data[3], user_data[4], user_data[5],))
        match_id = c.fetchone()

        if match_id is not None:
            match_data = get_match_data(match_id[0])
            await message.answer_photo(str(match_data[9]), unpack_ad(match_data), reply_markup=keyboards.tinder_keyboard)
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
    F.text == 'Deactivate my profile 😴'
)
async def deactivate(message: types.Message, state: FSMContext):
    c.execute("""
        UPDATE users
        SET gender = ?, gender_goals = ?, ad_text = ?
        WHERE id = ?
    """, (2, 3, '-', message.from_user.id,))
    c.execute('''DELETE FROM reactions WHERE id = ?''', (message.from_user.id,))
    c.execute('''DELETE FROM reactions WHERE match_id = ?''', (message.from_user.id,))
    await message.answer("Sorry to seeing you go😞\nYour ad and data have been deleted from us!\n"
                         "But you can always get back by typing /start or clicking on a button👇!",
                         reply_markup=keyboards.return_keyboard)


@router.message(
    Matches.action
)
async def perform_action(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'Like 💟':
        # insert or ignore to reactions
        c.execute(f'''
                INSERT OR IGNORE INTO matches (id, match_id, reaction)
                VALUES (?, ?, ?)
            ''', (message.from_user.id, data["awaiting"], 1))
        conn.commit()
        await moura.send_message(chat_id=data["awaiting"], text="You have a new like!", reply_markup=keyboards.see_likes_keyboard)
        # TODO: ONLY LAST INCOMING LIKE WILL BE VISIBLE
        await message.answer("Like was sent!")  # reply_markup=awaiting_keyboard)
        await state.set_state(Matches.awaiting)

    elif message.text == 'Next ⏩️':
        c.execute(f'''
                        INSERT OR IGNORE INTO matches (id, match_id, reaction)
                        VALUES (?, ?, ?)
                    ''', (message.from_user.id, data["awaiting"], 0))
        conn.commit()
        await message.answer("Okay, next one?",
                             reply_markup=keyboards.awaiting_keyboard)
        await state.set_state(Matches.awaiting)
    elif message.text == 'Complain ‼️':
        c.execute(f'''
                        INSERT OR IGNORE INTO matches (id, match_id, reaction)
                        VALUES (?, ?, ?)
                    ''', (message.from_user.id, data["awaiting"], 0))
        conn.commit()
        await message.answer("Please forward this ad to @heliumwer, he will deal with this person!", reply_markup=keyboards.awaiting_keyboard)
        await state.set_state(Matches.awaiting)


@dp.message(F.text == "Look at my likes!💟")
async def look_at_like(message: types.Message, state: FSMContext):
    c.execute('''
            SELECT id
            FROM reactions
            WHERE match_id = ? AND reaction = 1
            LIMIT 1
            ''', (message.from_user.id,))
    res = c.fetchone()
    if res is not None:  # we have likes left
        match_id = res[0]
        c.execute('''
            SELECT *
            FROM users
            WHERE id = ?
            LIMIT 1
        ''', (match_id,))
        match_data = c.fetchone()
        await state.update_data(awaiting=match_id)
        await message.answer_photo(str(match_data[9]), unpack_ad(match_data), reply_markup=keyboards.likes_keyboard)
    else:  # no likes left
        await state.set_state(Matches.awaiting)
        await message.answer("No more likes, wish to continue?", reply_markup=keyboards.awaiting_keyboard)


@dp.message(F.text == "Match 💟")
async def match(message: types.Message, state: FSMContext):
    data = await state.get_data()
    c.execute(f'''
                    UPDATE reactions
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
    logging.info("MATCHID: "+str(int(data['awaiting'])))
    await message.answer(f"Write to [your new match\!](tg://user?id={int(data['awaiting'])})", parse_mode=ParseMode.MARKDOWN_V2)
    await look_at_like(message, state)  # view next like
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
    await message.answer("Okay, next one!")
    await look_at_like(message, state)  # view next like


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
    await message.answer("Please forward this ad to @heliumwer, he will deal with this person!")
    await look_at_like(message, state)  # view next like
















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
