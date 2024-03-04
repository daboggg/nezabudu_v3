from aiogram.utils.formatting import as_key_value, Italic, as_list, Bold

from parser_v3.reminder import Reminder
from utils.from_datetime_to_str import datetime_to_str


def get_reminder_info(dialog_manager):
    reminder: Reminder = dialog_manager.dialog_data.get("reminder")
    job = dialog_manager.dialog_data.get("job")
    item = []
    if rd := reminder.period:
        item.append(as_key_value("♾", Italic(rd)))
    reminder_info = as_list(
        Bold("💡 Напоминание запланировано.\n"),
        as_key_value("⏰", Italic(datetime_to_str(job.next_run_time))),
        *item,
        as_key_value("📝", Italic(reminder.message)),

    ).as_html()
    return reminder_info
