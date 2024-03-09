from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.formatting import Italic
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.actions import get_reminder, edit_reminder
from bot.state_groups import EditReminds
from parser_v3.reminder import Reminder
from utils.converter import conv_voice

edit_reminder_handlers = Router()


@edit_reminder_handlers.callback_query(F.data.startswith("edit_remind"))
async def start_edit_reminder(callback: CallbackQuery, state: FSMContext, apscheduler: AsyncIOScheduler):
    job_id = callback.data.split(":")[1]
    hide_kb_id = callback.data.split(":")[2]
    apscheduler.remove_job(hide_kb_id)
    job = apscheduler.get_job(job_id)

    await callback.answer()
    await state.update_data(job_id=job_id)
    await callback.message.edit_text(f"👉 {job.kwargs.get('text')}")
    await callback.message.answer(Italic("✏️ 🎤 введите время и текст напоминания").as_html())
    await state.set_state(EditReminds.get_remind_time)


@edit_reminder_handlers.message(EditReminds.get_remind_time, F.text | F.voice)
async def get_text_or_voice(message: Message, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler):
    reminder = Reminder()
    try:
        reminder = await get_reminder(message)
        await state.update_data(reminder=reminder)
    except Exception as e:
        if message.text:
            reminder.message = message.text
        elif message.voice:
            reminder.message = await conv_voice(message,message.bot)
        await state.update_data(reminder=reminder)

    await edit_reminder(message, bot, state, apscheduler)


@edit_reminder_handlers.message(EditReminds.get_remind_time)
async def other_msg(message: Message):
    await message.answer(Italic("✏️ 🎤 введите время напоминания").as_html())
