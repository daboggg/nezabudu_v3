from aiogram.types import Message
from aiogram_dialog import DialogManager

from db.db_actions import add_remind_to_db
from parser_v3.parse import parse
from parser_v3.reminder import Reminder
from scheduler.scheduler_actions import add_job_to_scheduler
from utils.converter import conv_voice


async def get_reminder(event: Message)-> Reminder:
    if event.text:
        return parse(event.text)
    elif event.voice:
        text = await conv_voice(event, event.bot)
        return parse(text)


async def add_reminder(dialog_manager: DialogManager):
    job = await add_job_to_scheduler(dialog_manager)
    dialog_manager.dialog_data["job"] = job
    await add_remind_to_db(dialog_manager, job.id)