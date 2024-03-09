import json
import operator
from datetime import datetime
from typing import Any

from aiogram.types import CallbackQuery
from aiogram.utils.formatting import as_key_value, Italic, as_list, Bold
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Button, Back, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format, Case
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.state_groups import ListOfReminders
from db.db_actions import get_tasks_from_db_by_user_id, get_task_from_db
from models import Task
from utils.from_datetime_to_str import datetime_to_short_str, datetime_to_str


async def get_tasks(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id
    result = list()
    tasks: list[Task] = await get_tasks_from_db_by_user_id(user_id)
    for task in tasks:
        datetime_str = None
        text = task.text
        if task.period:
            datetime_str = task.period
        else:
            params: dict = json.loads(task.params)
            run_date = params.get("run_date")
            dt = datetime.fromisoformat(run_date)
            datetime_str = datetime_to_short_str(dt)
        result.append((datetime_str, text, task.id))

    return {
        "reminders": result,
        "count": str(len(tasks)),
    }


async def get_reminder(dialog_manager: DialogManager, **kwargs):
    job_id = dialog_manager.dialog_data.get("job_id")
    apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get("apscheduler")

    job = apscheduler.get_job(job_id)
    task: Task = await get_task_from_db(job_id)

    item = []
    if rd := task.period:
        item.append(as_key_value("♾", Italic(rd)))
    remind_info = as_list(
        as_key_value("⏰", Italic(datetime_to_str(job.next_run_time))),
        *item,
        as_key_value("📝", Italic(task.text)),

    ).as_html()

    return {"remind_info": remind_info}

async def on_reminder_selected(callback: CallbackQuery, widget: Any,
                               manager: DialogManager, job_id: str):
    manager.dialog_data["job_id"] = job_id
    await manager.switch_to(ListOfReminders.show_reminder)


async def on_delete_selected(callback: CallbackQuery, button: Button,
                     dialog_manager: DialogManager):
    apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get("apscheduler")
    apscheduler.remove_job(dialog_manager.dialog_data.get("job_id"))
    await callback.answer("напоминание удалено")
    del dialog_manager.dialog_data["job_id"]
    await dialog_manager.switch_to(ListOfReminders.start)


# диалог список напоминаний
list_reminders_dialog = Dialog(
    Window(
        Const(Bold("📄 Список напоминаний:").as_html()),
        Case(
            {
                "0": Const("            🫲   🫱"),
                ...: Format("           всего: {count} 👇")
            },
            selector="count"
        ),
        ScrollingGroup(
            Select(
                Format("{item[0]} {item[1]}"),
                id="s_reminders",
                item_id_getter=operator.itemgetter(2),
                items="reminders",
                on_click=on_reminder_selected,
            ),
            id='scroll',
            width=1,
            height=7
        ),
        state=ListOfReminders.start,
        getter=get_tasks,
    ),
    Window(
        Format('{remind_info}'),
        Back(Const("Назад")),
        Button(Const("Удалить"),id='delete_reminder', on_click=on_delete_selected),
        state=ListOfReminders.show_reminder,
        getter=get_reminder,
    ),
)
