from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.formatting import Bold, Strikethrough
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.actions import get_reminder, add_reminder
from bot.state_groups import EditReminds
from parser_v3.reminder import Reminder

edit_reminder_handlers = Router()

@edit_reminder_handlers.callback_query(F.data.startswith("edit_remind"))
async def start_edit_reminder(callback: CallbackQuery, state: FSMContext, apscheduler: AsyncIOScheduler):
    job_id = callback.data.split(":")[1]
    hide_kb_id = callback.data.split(":")[2]
    apscheduler.remove_job(hide_kb_id)

    # todo добавить текс из джоб в стейт

    await callback.message.answer("введите время напоминания")
    await callback.answer()
    await state.set_state(EditReminds.get_remind_time)


@edit_reminder_handlers.message(EditReminds.get_remind_time, F.text | F.voice)
async def edit_reminder(message: Message, state: FSMContext, apscheduler: AsyncIOScheduler):
    pass
    # reminder=Reminder()
    # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    # try:
    #     reminder = await get_reminder(message)
    #     if reminder.message:
    #         await state.update_data(reminder=reminder)
    #         await add_reminder(message, apscheduler, state)
    #         print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    #     else:
    #         state_data = await state.get_data()
    #         reminder.message = state_data.get("job").kwargs.get("text")
    #         await state.update_data(reminder=reminder)
    #         await add_reminder(message, apscheduler, state)
    #         print('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT')
    # except Exception as e:
    #     reminder.message = message.text
    #     await state.update_data(reminder=reminder)
    #     await add_reminder(message, apscheduler, state)
    #     print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")



@edit_reminder_handlers.message(EditReminds.get_remind_time)
async def other_msg(message: Message):
    await message.answer("введите время напоминания")

    #
    # part_msg = callback.message.text.split("\n")
    # msg = Bold(f"{part_msg[0].replace('запланировано', 'отменено')}\n").as_html() + Strikethrough(
    #     '\n'.join(part_msg[1:])).as_html()
    #
    # await callback.message.edit_text(msg)
