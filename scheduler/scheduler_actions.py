import json
import logging

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.handlers.send_message_handlers import send_reminder
from db.db_actions import get_tasks_from_db
from parser_v3.reminder import Reminder

logger = logging.getLogger(__name__)


# добавление задания в скедулер
async def add_job_to_scheduler(
        message: Message,
        apscheduler: AsyncIOScheduler,
        state: FSMContext,
) -> Job:
    state_data = await state.get_data()
    reminder: Reminder = state_data.get("reminder")
    user_id = message.from_user.id

    job = apscheduler.add_job(
        send_reminder,
        **reminder.params,
        name=str(user_id),
        kwargs={
            'apscheduler': apscheduler,
            'bot': message.bot,
            'user_id': user_id,
            'text': reminder.message,
        }
    )
    return job

# изменение задания в скедулере
async def edit_job_to_scheduler(
        apscheduler: AsyncIOScheduler,
        bot: Bot,
        state: FSMContext,
):
    state_data = await state.get_data()
    reminder: Reminder = state_data.get("reminder")
    job_id = state_data.get("job_id")
    job = apscheduler.get_job(job_id)

    params = reminder.params
    message = reminder.message

    if params and message:
        apscheduler.reschedule_job(
            job_id=str(job_id),
            **params
        )
        return apscheduler.modify_job(
            job_id=str(job_id),
            kwargs={
                'apscheduler': apscheduler,
                'bot': bot,
                'user_id': int(job.name),
                'text': message,
            }
        )
    elif params:
        return apscheduler.reschedule_job(
            job_id=str(job_id),
            **params
        )
    else:
        return apscheduler.modify_job(
            job_id=str(job_id),
            kwargs={
                'apscheduler': apscheduler,
                'bot': bot,
                'user_id': int(job.name),
                'text': message,
            }
        )


# восстановление заданий из базы данных
async def recovery_job_to_scheduler(apscheduler: AsyncIOScheduler, bot: Bot):
    if tasks := await get_tasks_from_db():
        for task in tasks:
            tmp = json.loads(task.params)

            apscheduler.add_job(
                send_reminder,
                **tmp,
                id=task.id,
                name=str(task.user_id),
                kwargs={
                    'apscheduler': apscheduler,
                    'bot': bot,
                    'user_id': task.user_id,
                    'text': task.text,
                }
            )
