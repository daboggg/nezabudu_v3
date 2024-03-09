from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.formatting import Italic
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.actions import get_reminder, add_reminder
from bot.state_groups import MainDialog
from utils.converter import conv_voice

add_reminder_handlers = Router()


# добавляем текст к напоминанию
@add_reminder_handlers.message(MainDialog.get_text, F.text | F.voice)
async def set_reminder(message: Message, apscheduler: AsyncIOScheduler, state: FSMContext) -> None:
    state_data = await state.get_data()
    if message.text:
        state_data.get("reminder").message = message.text
    elif message.voice:
        text = await conv_voice(message, message.bot)
        state_data.get("reminder").message = text
    await add_reminder(message, apscheduler, state)


@add_reminder_handlers.message(MainDialog.get_text)
async def other_text(message: Message) -> None:
    await message.answer(Italic("✏️ 🎤 введите текст напоминания").as_html())


@add_reminder_handlers.message(F.text | F.voice)
async def set_reminder(message: Message, apscheduler: AsyncIOScheduler, state: FSMContext) -> None:
    try:
        reminder = await get_reminder(message)
        await state.update_data(reminder=reminder)
        if reminder.message:
            await add_reminder(message, apscheduler, state)
        else:
            await state.set_state(MainDialog.get_text)
            await message.answer(Italic("✏️ 🎤 введите текст напоминания").as_html())
    except Exception as e:
        print(e)
        await other_msg(message)


@add_reminder_handlers.message()
async def other_msg(message: Message) -> None:
    await message.answer(Italic("✏️ 🎤 пожалуйста введите время и текст сообщения").as_html())
