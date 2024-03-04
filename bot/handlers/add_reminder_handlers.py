from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.actions import get_reminder, add_reminder
from utils.reminder_info import get_reminder_info

add_reminder_handlers = Router()


@add_reminder_handlers.message(F.text | F.voice)
async def set_reminder(message: Message, apscheduler: AsyncIOScheduler, state: FSMContext, ):
    try:
        reminder = await get_reminder(message)
        await state.update_data(reminder=reminder)
        if reminder.message:
            await add_reminder(message, apscheduler, state)

        else:
            pass
    #     todo !!!!!!!!!!!!!!!!!!!!!!!!!!
    except Exception as e:
        print(e)




@add_reminder_handlers.message()
async def other_msg(message: Message):
    await message.answer("пожалуйста введите время и текст сообщения")
