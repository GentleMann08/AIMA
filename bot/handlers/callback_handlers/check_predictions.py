from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.menu import Menu

predictions_router = Router()

@predictions_router.callback_query(F.data == 'check_predictions')
async def predictions(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get("last_message_id")

    if last_message_id:
        await callback_query.message.chat.delete_message(message_id=last_message_id)

    keyboard = await Menu.predictions()
    await callback_query.answer('Feature under development')
    new_message = await callback_query.message.answer(
        text="Function is now available. Please choose another option.",
        reply_markup=keyboard
    )

    await state.update_data(last_message_id=new_message.message_id)