from .operations.keyboard_operations import KeyboardOperations

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