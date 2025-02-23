from aiogram.fsm.state import State, StatesGroup

class AddUser(StatesGroup):
    waiting_for_username = State()