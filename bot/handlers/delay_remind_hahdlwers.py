from datetime import datetime, timedelta

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.formatting import as_list, Bold, as_key_value, Italic
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.actions import get_reminder, add_reminder
from bot.state_groups import RescheduleReminds
from parser_v3.reminder import Reminder
from utils.from_datetime_to_str import datetime_to_str

delay_remind_handlers = Router()


# отложить напоминание
@delay_remind_handlers.callback_query(F.data.startswith("delay_remind"))
async def delay_remind(callback: CallbackQuery, apscheduler: AsyncIOScheduler):
    tmp = callback.data.split(":")
    job_id = tmp[1]
    res = {tmp[2]:int(tmp[3])}
    job: Job = apscheduler.reschedule_job(job_id=job_id, trigger='date',
                                          run_date=datetime.now() + timedelta(**res))
    remind_info = as_list(
        Bold("💡 Напоминание отложено.\n"),
        as_key_value("⏰", Italic(datetime_to_str(job.next_run_time))),
        as_key_value("📝", Italic(job.kwargs.get("text"))),
    ).as_html()

    await callback.answer()
    await callback.message.edit_text(remind_info)


# напоминание выполнено
@delay_remind_handlers.callback_query(F.data.startswith("done_remind"))
async def delay_remind(callback: CallbackQuery, apscheduler: AsyncIOScheduler):
    tmp = callback.data.split(":")
    job_id = tmp[1]

    job: Job = apscheduler.get_job(job_id)

    format_text = as_list(
        Bold("\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──"),
        f"✔️ 👉{job.kwargs.get('text')}👈",
        Bold("\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──"),
    ).as_html()
    await callback.answer()
    await callback.message.edit_text(format_text)
    job.remove()








# переназначить напоминание
@delay_remind_handlers.callback_query(F.data.startswith("reschedule_remind"))
async def reschedule_remind(callback: CallbackQuery, state: FSMContext, apscheduler: AsyncIOScheduler):
    tmp = callback.data.split(":")
    job_id = tmp[1]
    job = apscheduler.get_job(job_id)
    await state.update_data(job_id=job_id, user_id=int(job.name), text=job.kwargs.get("text"))
    job.remove()
    await callback.answer()
    await callback.message.edit_text("введите время напоминания")
    await state.set_state(RescheduleReminds.get_remind)


@delay_remind_handlers.message(RescheduleReminds.get_remind, F.text | F.voice)
async def get_remind(message: Message, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler):
    state_data = await state.get_data()
    reminder = Reminder()

    try:
        reminder = await get_reminder(message)
        await state.update_data(reminder=reminder)
        # если в напоминании присутствует текст сообщения, то отправляем на добавления задания
        if reminder.message:
            await add_reminder(message, apscheduler, state)
        else:
            reminder.message = state_data.get("text")
            await add_reminder(message, apscheduler, state)

    except Exception as e:
        await message.answer('введите время напоминания')



@delay_remind_handlers.message(RescheduleReminds.get_remind)
async def not_text_not_voice(message: Message):
    await message.answer("введите время напоминания")
