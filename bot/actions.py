from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.keyboards.delete_or_edit_reminder_keyboard import cancel_or_edit_kb
from db.db_actions import add_remind_to_db, edit_task_to_db
from parser_v3.parse import parse
from parser_v3.reminder import Reminder
from scheduler.scheduler_actions import add_job_to_scheduler, edit_job_to_scheduler
from utils.converter import conv_voice
from text_responses.reminder_info import get_reminder_info, edit_reminder_info


# получает объект Reminder из парсера
async def get_reminder(event: Message) -> Reminder:
    if event.text:
        return parse(event.text)
    elif event.voice:
        text = await conv_voice(event, event.bot)
        return parse(text)


# добавляет напоминание в скедулер и бд
async def add_reminder(message: Message, apscheduler: AsyncIOScheduler, state: FSMContext) -> None:
    job = await add_job_to_scheduler(message, apscheduler, state)
    await add_remind_to_db(message, state, job.id)
    reminder_info = await get_reminder_info(state, job)
    await state.clear()

    # создать id для удаления клавиатуры
    hide_kb_id = f"{message.from_user.id}{datetime.now().second}"

    # ответ об установке напоминания  с клавиатурой для отмены или редактирования
    msg = await message.answer(reminder_info, reply_markup=cancel_or_edit_kb(job.id, hide_kb_id))

    # удалить клавиатуру через промежуток времени
    date = datetime.now() + timedelta(seconds=15)
    apscheduler.add_job(edit_msg, "date", id=hide_kb_id, run_date=date, kwargs={"message": msg})


# редактирует напоминание в скедулер и бд
async def edit_reminder(message: Message, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler):
    job = await edit_job_to_scheduler(apscheduler, bot, state)
    await edit_task_to_db(state)
    reminder_info = await edit_reminder_info(state, job)
    await state.clear()

    # todo исправить reminder_info

    # создать id для удаления клавиатуры
    hide_kb_id = f"{message.from_user.id}{datetime.now().second}"

    # ответ об установке напоминания  с клавиатурой для отмены или редактирования
    msg = await message.answer(reminder_info, reply_markup=cancel_or_edit_kb(job.id, hide_kb_id))

    # удалить клавиатуру через промежуток времени
    date = datetime.now() + timedelta(seconds=15)
    apscheduler.add_job(edit_msg, "date", id=hide_kb_id, run_date=date, kwargs={"message": msg})




# удаление клавиатуры
async def edit_msg(message: Message) -> None:
    await message.edit_reply_markup(reply_markup=None)
