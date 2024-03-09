from aiogram.fsm.state import StatesGroup, State


class MainDialog(StatesGroup):
    get_text = State()

class EditReminds(StatesGroup):
    get_remind_time = State()

class RescheduleReminds(StatesGroup):
    get_remind = State()

class ListOfReminders(StatesGroup):
    start = State()
    show_reminder = State()

class SetupReminders(StatesGroup):
    select_setting = State()
    select_auto_delay = State()
    select_buttons_delay = State()
