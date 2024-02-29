import json
import operator
from datetime import datetime
from typing import Any

from aiogram.types import CallbackQuery
from aiogram.utils.formatting import as_key_value, Italic, as_list, Bold
from aiogram_dialog import Dialog, Window, DialogManager, Data
from aiogram_dialog.widgets.kbd import Select, Column, Button, Back, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format, Case
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.state_groups import MainDialog


async def get_reminder(dialog_manager: DialogManager, **kwargs):

    return {
        "reminder": "REMINDER",
    }


# async def get_reminder(dialog_manager: DialogManager, **kwargs):
#     reminder_id = dialog_manager.dialog_data.get("reminder_id")
#     apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get("apscheduler")
#
#     job = apscheduler.get_job(reminder_id)
#     reminder: Remind = await get_task_from_db(int(reminder_id))
#
#     item = []
#     if rd := reminder.period:
#         item.append(as_key_value("♾", Italic(rd)))
#     remind_info = as_list(
#         as_key_value("⏰", Italic(datetime_to_str(job.next_run_time))),
#         *item,
#         as_key_value("📝", Italic(reminder.text)),
#
#     ).as_html()
#
#     return {"remind_info": remind_info}
#
# async def on_reminder_selected(callback: CallbackQuery, widget: Any,
#                                manager: DialogManager, reminder_id: str):
#     manager.dialog_data["reminder_id"] = reminder_id
#     await manager.switch_to(ListOfReminders.show_reminder)
#
#
# async def on_delete_selected(callback: CallbackQuery, button: Button,
#                      dialog_manager: DialogManager):
#     apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get("apscheduler")
#     apscheduler.remove_job(dialog_manager.dialog_data.get("reminder_id"))
#     await callback.answer("напоминание удалено")
#     del dialog_manager.dialog_data["reminder_id"]
#     await dialog_manager.switch_to(ListOfReminders.start)


# диалог список напоминаний
main_dialog = Dialog(
    Window(
        Format('{reminder}'),
        # Back(Const("Назад")),
        # Button(Const("Удалить"),id='delete_reminder', on_click=on_delete_selected),
        state=MainDialog.get_reminder,
        getter=get_reminder,
    ),
)