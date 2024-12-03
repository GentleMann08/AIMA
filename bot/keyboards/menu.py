from .operations.keyboard_operations import KeyboardOperations
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

class Menu:
    @staticmethod
    async def start():
        buttons_dict = {
            "Subscribe to bonds 🔔": "subscribe_to_bonds",
            "Check predictions 📈": "check_predictions"
        }
        
        keyboard = await KeyboardOperations.create_base_keyboard(buttons=buttons_dict)
        return keyboard
    
    @staticmethod
    async def to_start():
        buttons_dict = {
            "Menu": "to_start"
        }
        
        keyboard = await KeyboardOperations.create_base_keyboard(buttons=buttons_dict)
        return keyboard
    
    @staticmethod
    async def predictions():

        buttons_dict = {"⬅️ Menu": "to_start"}

        keyboard = await KeyboardOperations.create_base_keyboard(buttons=buttons_dict)
        return keyboard
    
    @staticmethod
    async def to_bonds():
        buttons = {
            'Gazprom 💙': 'gazp_bond',
            'T-Group 💛': 'tinkoff_bond',
            'Sberbank 💚': 'sber_bond',
            'Beeline 🐝': 'beeline_bond',
            'Rosneft 🛢': 'rosneft_bond'
        }

        buttons_dict = buttons | {"⬅️ Menu": "to_start"}

        keyboard = await KeyboardOperations.create_base_keyboard(buttons=buttons_dict)
        return keyboard
    
    @staticmethod
    async def subscribe(bond_name, state: FSMContext):
        data = await state.get_data()
        subscriptions = data.get("subscriptions", [])
        if subscriptions is None:
            subscriptions = []

        if bond_name not in subscriptions:
            buttons = {f'Not subscribed ❌': f'{bond_name}_subscribe/unsubscribe'}
        else:
            buttons = {f'Subscribed ✅': f'{bond_name}__subscribe/unsubscribe'}

        buttons_dict = buttons | {"⬅️ To other bonds": "subscribe_to_bonds"}

        keyboard = await KeyboardOperations.create_base_keyboard(buttons=buttons_dict)
        return keyboard
