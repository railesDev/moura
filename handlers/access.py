from bot import router, F, types, FSMContext
import keyboards
from states import User
import consts


@router.message((F.text.upper() == consts.access_code))
async def access(message: types.Message, state: FSMContext) -> None:
    await state.update_data(id=message.from_user.id)
    # ask for gender
    await message.answer_photo(consts.gender_photo,
                               consts.gender_caption,
                               reply_markup=keyboards.keyboard_gender)
    await state.set_state(User.gender)  # setting state that we wait for gender
