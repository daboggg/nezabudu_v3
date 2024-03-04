import json
import logging

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.handlers.send_remind_hendlers import send_reminder
from parser_v3.reminder import Reminder

logger = logging.getLogger(__name__)


# добавление задания в скедулер
async def add_job_to_scheduler(
        dialog_manager: DialogManager,
) -> Job:
    apscheduler = dialog_manager.middleware_data.get("apscheduler")
    reminder: Reminder = dialog_manager.dialog_data.get("reminder")
    user_id = dialog_manager.event.from_user.id

    job = apscheduler.add_job(
        send_reminder,
        **reminder.params,
        name=str(user_id),
        kwargs={
            'apscheduler': apscheduler,
            'bot': dialog_manager.event.bot,
            'user_id': user_id,
            'text': reminder.message,
        }
    )
    return job.id

# изменение задания в скедулере
# async def edit_job_to_scheduler(
#         apscheduler: AsyncIOScheduler,
#         bot: Bot,
#         state: FSMContext,
# ):
#     state_data = await state.get_data()
#
#     params = state_data.get("params", None)
#     message = state_data.get("message", None)
#     job_id = state_data.get("job_id")
#     job = apscheduler.get_job(job_id)
#
#     if params and message:
#         apscheduler.reschedule_job(
#             job_id=str(job_id),
#             **params
#         )
#         return apscheduler.modify_job(
#             job_id=str(job_id),
#             kwargs={
#                 'apscheduler': apscheduler,
#                 'bot': bot,
#                 'chat_id': int(job.name),
#                 'text': message,
#             }
#         )
#     elif params:
#         return apscheduler.reschedule_job(
#             job_id=str(job_id),
#             **params
#         )
#     else:
#         return apscheduler.modify_job(
#             job_id=str(job_id),
#             kwargs={
#                 'apscheduler': apscheduler,
#                 'bot': bot,
#                 'chat_id': int(job.name),
#                 'text': message,
#             }
#         )
#
#
# # восстановление заданий из базы данных
# async def recovery_job_to_scheduler(apscheduler: AsyncIOScheduler, bot: Bot):
#     if tasks := await get_tasks_from_db():
#         for task in tasks:
#             tmp = json.loads(task.params)
#
#             apscheduler.add_job(
#                 send_reminder,
#                 **tmp,
#                 id=str(task.id),
#                 name=str(task.chat_id),
#                 kwargs={
#                     'apscheduler': apscheduler,
#                     'bot': bot,
#                     'chat_id': task.chat_id,
#                     'text': task.text,
#                 }
#             )
