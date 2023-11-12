from aiogram import types


kb_gender = [
        [types.KeyboardButton(text='I am a Guy ‍👨‍💼')],
        [types.KeyboardButton(text='I am a Lady ‍👩‍💼')],
        [types.KeyboardButton(text='Start over 🔄')]
    ]
keyboard_gender = types.ReplyKeyboardMarkup(keyboard=kb_gender,
                                            resize_keyboard=True,
                                            input_field_placeholder='Your gender?'
                                            )

kb_campus = [
        [types.KeyboardButton(text='Kantemirovskaya 🏭')],
        [types.KeyboardButton(text='Griboedova 🏨')],
        [types.KeyboardButton(text='Promyshlennaya 🏫')],
        [types.KeyboardButton(text='Sedova 🏠')],
        [types.KeyboardButton(text='Start over 🔄')]
    ]
keyboard_campus = types.ReplyKeyboardMarkup(keyboard=kb_campus,
                                            resize_keyboard=True,
                                            input_field_placeholder='Choose a campus'
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
            [types.KeyboardButton(text='Start over 🔄')]
        ]

kb_griba = [
            [types.KeyboardButton(text='History 📜')],
            [types.KeyboardButton(text='Mediacommunications 📱')],
            [types.KeyboardButton(text='Philology 📚')],
            [types.KeyboardButton(text='Politology 🏛️')],
            [types.KeyboardButton(text='Vostokovedenie ⛩️')],
            [types.KeyboardButton(text='Start over 🔄')]
        ]

kb_proma = [
            [types.KeyboardButton(text='Design 🎨')],
            [types.KeyboardButton(text='UAGS 🏢')],
            [types.KeyboardButton(text='Start over 🔄')]
        ]

course_kb = [
        [types.KeyboardButton(text='1 👶')],
        [types.KeyboardButton(text='2 🧒')],
        [types.KeyboardButton(text='3 🧔‍')],
        [types.KeyboardButton(text='4 👴')],
        [types.KeyboardButton(text='Start over 🔄')]
    ]

course_keyboard = types.ReplyKeyboardMarkup(keyboard=course_kb,
                                            resize_keyboard=True,
                                            input_field_placeholder='Choose course #'
                                            )

gendergoals_kb = [
        [types.KeyboardButton(text='Guys 👨')],
        [types.KeyboardButton(text='Ladies ‍👩')],
        [types.KeyboardButton(text='Both 🤷')],
        [types.KeyboardButton(text='Start over 🔄')]
    ]

gendergoals_keyboard = types.ReplyKeyboardMarkup(keyboard=gendergoals_kb,
                                                 resize_keyboard=True,
                                                 input_field_placeholder='Choose preferences'
                                                 )

photo_kb = [
        [types.KeyboardButton(text='No photo ❌')],
        [types.KeyboardButton(text='Start over 🔄')]
    ]

photo_keyboard = types.ReplyKeyboardMarkup(keyboard=photo_kb,
                                           resize_keyboard=True,
                                           input_field_placeholder='Upload photo/refuse'
                                           )

last_kb = [
        [types.KeyboardButton(text='Publish 🏹!')],
        [types.KeyboardButton(text='Start over 🔄')],
    ]

last_keyboard = types.ReplyKeyboardMarkup(keyboard=last_kb,
                                          resize_keyboard=True,
                                          input_field_placeholder='Ready to go?'
                                          )

awaiting_kb = [
        [types.KeyboardButton(text='🔮Show me people!🔮')],
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
