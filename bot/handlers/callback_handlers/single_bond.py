from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.menu import Menu

choose_bond_router = Router()

@choose_bond_router.callback_query(F.data.endswith('_bond'))
async def single_bond(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get("last_message_id")
    bond = callback_query.data.split('_')[0]

    if last_message_id:
        await callback_query.message.chat.delete_message(message_id=last_message_id)

    keyboard = await Menu.subscribe(bond_name=bond, state=state)
    await callback_query.answer('Choose a bond to subscribe to')
    new_message = await callback_query.message.answer(
        text=bond,
        reply_markup=keyboard
    )

    await state.update_data(last_message_id=new_message.message_id)