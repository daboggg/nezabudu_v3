from aiogram.fsm.state import StatesGroup, State


class MainDialog(StatesGroup):
    set_reminder = State()


