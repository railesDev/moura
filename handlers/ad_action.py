from bot import moura, router, F, types, FSMContext, ReplyKeyboardRemove
from bot import c, conn
from states import User
import dboper
import consts
import keyboards


@router.message(
    User.action,
    F.text.in_(consts.actions)
)
async def perform_action(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == consts.actions[0]:
        dboper.react(conn, c, message.from_user.id, data["awaiting"], 1)
        await moura.send_message(chat_id=data["awaiting"],
                                 text=consts.got_like_caption,
                                 reply_markup=keyboards.see_likes_keyboard)
        await message.answer("Like was sent!")  # reply_markup=awaiting_keyboard)
        # TODO: WILL NEXT AD BE SENT?
        await state.set_state(User.awaiting)

    elif message.text == consts.actions[1]:
        dboper.react(conn, c, message.from_user.id, data["awaiting"], 0)
        await message.answer("Okay, next one?",
                             reply_markup=keyboards.awaiting_keyboard)
        # TODO: 100% NEXT AD WILL BE SENT
        await state.set_state(User.awaiting)

    elif message.text == consts.actions[2]:
        dboper.react(conn, c, message.from_user.id, data["awaiting"], 0)
        await message.answer(consts.complain_caption,
                             reply_markup=keyboards.awaiting_keyboard)
        await state.set_state(User.awaiting)
