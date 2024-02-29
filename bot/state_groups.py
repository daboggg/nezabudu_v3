from aiogram.fsm.state import StatesGroup, State


class MainDialog(StatesGroup):
    get_reminder = State()


