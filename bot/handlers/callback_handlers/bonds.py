from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.menu import Menu

bonds_router = Router()

@bonds_router.callback_query(F.data == 'subscribe_to_bonds')
async def all_bonds(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get("last_message_id")

    if last_message_id:
        await callback_query.message.chat.delete_message(message_id=last_message_id)

    keyboard = await Menu.to_bonds(state)
    await callback_query.answer('Choose a bond to subscribe to')
    new_message = await callback_query.message.answer(
        text="Bonds (not all are currently supported):",
        reply_markup=keyboard
    )

    await state.update_data(last_message_id=new_message.message_id)

@bonds_router.callback_query(F.data.endswith('_bond'))
async def single_bond(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get("last_message_id")
    bond = callback_query.data.split('_')[0]

    if last_message_id:
        await callback_query.message.chat.delete_message(message_id=last_message_id)

    keyboard = await Menu.subscribe(bond_name=bond, state=state)
    new_message = await callback_query.message.answer(
        text=f"(here is {bond}'s description)",
        reply_markup=keyboard
    )


    await state.update_data(last_message_id=new_message.message_id)
    await state.update_data(last_message_text=new_message.text)

@bonds_router.callback_query(F.data.endswith('_subscribe/unsubscribe'))
async def subscribtion(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get("last_message_id")
    last_message_text = data.get("last_message_text")
    subscriptions = data.get("subscriptions", [])

    bond_name = callback_query.data.split('_')[0]

    if bond_name not in subscriptions:
        subscriptions.append(bond_name)
        await callback_query.answer(f'You have subscribed to {bond_name.upper()}!')
    else:
        subscriptions.remove(bond_name)
        await callback_query.answer(f'You have unsubscribed from {bond_name.upper()}!')
    
    if last_message_id:
        await callback_query.message.chat.delete_message(message_id=last_message_id)

    await state.update_data(subscriptions=subscriptions)
    keyboard = await Menu.subscribe(bond_name=bond_name, state=state)
    new_message = await callback_query.message.answer(
        text=last_message_text,
        reply_markup=keyboard
    )

    await state.update_data(last_message_id=new_message.message_id)