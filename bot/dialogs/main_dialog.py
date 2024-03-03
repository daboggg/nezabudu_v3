import json
import operator
from datetime import datetime
from typing import Any

from aiogram.types import CallbackQuery
from aiogram.utils.formatting import as_key_value, Italic, as_list, Bold
from aiogram_dialog import Dialog, Window, DialogManager, Data
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select, Column, Button, Back, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format, Case
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.actions import get_reminder
from bot.state_groups import MainDialog


async def getter_set_reminder(dialog_manager: DialogManager, **kwargs):

    return {
        "text": "пожалуйста введите время и текст напоминания",
    }

async def set_reminder(event, widget, dialog_manager: DialogManager, *_):
    try:
        reminder = await get_reminder(event)
        print(reminder)
    except Exception as e:
        print(e)




# диалог список напоминаний
main_dialog = Dialog(
    Window(
        Format('{text}'),
        MessageInput(set_reminder),
        # Back(Const("Назад")),
        # Button(Const("Удалить"),id='delete_reminder', on_click=on_delete_selected),
        state=MainDialog.set_reminder,
        getter=getter_set_reminder,
    ),
)