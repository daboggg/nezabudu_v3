from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.actions import get_reminder, add_reminder
from bot.state_groups import MainDialog

add_reminder_handlers = Router()


@add_reminder_handlers.message(MainDialog.get_text, F.text)
async def set_reminder(message: Message, apscheduler: AsyncIOScheduler, state: FSMContext, ):
    state_data = await state.get_data()
    state_data.get("reminder").message = message.text
    await add_reminder(message, apscheduler, state)


@add_reminder_handlers.message(F.text | F.voice)
async def set_reminder(message: Message, apscheduler: AsyncIOScheduler, state: FSMContext, ):
    try:
        reminder = await get_reminder(message)
        await state.update_data(reminder=reminder)
        if reminder.message:
            await add_reminder(message, apscheduler, state)
        else:
            await state.set_state(MainDialog.get_text)
            await message.answer("введите текст напоминания")
    except Exception as e:
        print(e)
        await other_msg(message)


@add_reminder_handlers.message()
async def other_msg(message: Message):
    await message.answer("пожалуйста введите время и текст сообщения")
