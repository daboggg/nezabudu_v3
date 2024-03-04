from datetime import datetime, timedelta

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db.db_actions import add_remind_to_db
from parser_v3.parse import parse
from parser_v3.reminder import Reminder
from scheduler.scheduler_actions import add_job_to_scheduler
from utils.converter import conv_voice


# получает объект Reminder из парсера
async def get_reminder(event: Message)-> Reminder:
    if event.text:
        return parse(event.text)
    elif event.voice:
        text = await conv_voice(event, event.bot)
        return parse(text)


# добавляет напоминание в скедулер и бд
async def add_reminder(message: Message, apscheduler: AsyncIOScheduler, state: FSMContext,):
    job = await add_job_to_scheduler(message, apscheduler, state)
    # await add_remind_to_db(dialog_manager, job.id)



#     # удалить клавиатуру через промежуток времени
#     date = datetime.now() + timedelta(seconds=15)
#     apscheduler.add_job(edit_msg, "date", run_date=date, kwargs={"dialog_manager": dialog_manager})
#
#
# # удаление клавиатуры
# async def edit_msg(dialog_manager: DialogManager):
#     dialog_manager.bg(dialog_manager.event.from_user.id,dialog_manager.event.chat.id,dialog_manager.current_stack().id).dialog_data["show_buttons"] = False