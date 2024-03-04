import time
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.formatting import as_list
from apscheduler.schedulers.asyncio import AsyncIOScheduler



# функция для отправки напоминаний
async def send_reminder(
        apscheduler: AsyncIOScheduler,
        bot: Bot,
        user_id: int,
        text: str,
        **kwargs,
) -> None:
    # форматирование текста для напоминания
    # format_text = as_list(
    #     "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
    #     f"👉{text}👈",
    #     "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
    # )
    #
    # remind_id = str(time.time_ns())
    #
    # if msg := kwargs.get("message", None):
    #     try:
    #         await msg.edit_reply_markup(reply_markup=None)
    #     except TelegramBadRequest:
    #         pass

    # message = await bot.send_message(chat_id, format_text.as_html(), reply_markup=delay_kb(remind_id), parse_mode='HTML')
    message = await bot.send_message(user_id, text,  parse_mode='HTML')

    # job = apscheduler.add_job(
    #     send_reminder,
    #     run_date=datetime.now() + timedelta(minutes=15),
    #     id=remind_id,
    #     trigger='date',
    #     name=str(chat_id),
    #     kwargs={
    #         'apscheduler': apscheduler,
    #         'bot': bot,
    #         'chat_id': chat_id,
    #         'text': text,
    #         'message': message
    #     }
    # )
