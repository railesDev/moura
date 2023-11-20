from bot import moura
from bot import dp, router, F, types, FSMContext
import keyboards
from states import User
from bot import c, conn
import consts
import dboper


def goals_encoder(goals_data, decode=False):
    if decode:
        output = goals_data[0]*'Friendship 🤙, '+goals_data[1]*'Dates 👫, '+goals_data[2]*'Networking 🤝'
        return output
    else:
        code = ['Friendship 🤙' in goals_data, 'Dates 👫' in goals_data, 'Networking 🤝' in goals_data]
        return code


@router.message(
    User.finished,
    F.text == consts.publish_ad
)
async def register_finishing(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sdata = list(data.values())
    sdata[5] = goals_encoder(sdata[5])
    sdata = sdata[:5] + [sdata[5][0], sdata[5][1], sdata[5][2]] + sdata[6:]
    await message.answer(
        text=consts.published_ad_caption,
        reply_markup=keyboards.awaiting_keyboard
    )
    # Insert the user data into the table
    dboper.save_user(conn, c, sdata)
    await state.set_state(User.awaiting)
    # await state.update_data(awaiting=0)
