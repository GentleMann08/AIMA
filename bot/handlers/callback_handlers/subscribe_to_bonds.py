from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.menu import Menu

subscribe_router = Router()

@subscribe_router.callback_query(F.data == 'subscribe_to_bonds')
async def subscribe(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get("last_message_id")

    if last_message_id:
        await callback_query.message.chat.delete_message(message_id=last_message_id)

    keyboard = await Menu.to_bonds()
    await callback_query.answer('Choose a bond to subscribe to')
    new_message = await callback_query.message.answer(
        text="Bonds (not all are currently supported):",
        reply_markup=keyboard
    )

    await state.update_data(last_message_id=new_message.message_id)