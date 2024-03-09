import json
import time
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.formatting import as_list
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.keyboards.delay_keyboard import delay_kb
from db.db_actions import get_auto_delay_time


# функция для отправки напоминаний
async def send_reminder(
        apscheduler: AsyncIOScheduler,
        bot: Bot,
        user_id: int,
        text: str,
        **kwargs,
) -> None:
    auto_delay_time = await get_auto_delay_time(user_id)
    auto_delay_time = json.loads(auto_delay_time)

    # форматирование текста для напоминания
    format_text = as_list(
        "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
        f"👉{text}👈",
        "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
    )

    remind_id = str(time.time_ns())

    if msg := kwargs.get("message", None):
        try:
            # await msg.edit_reply_markup(reply_markup=None)
            await msg.delete()
        except TelegramBadRequest:
            pass

    message = await bot.send_message(user_id, format_text.as_html(), reply_markup=await delay_kb(remind_id, user_id), parse_mode='HTML')

    apscheduler.add_job(
        send_reminder,
        run_date=datetime.now() + timedelta(**auto_delay_time),
        id=remind_id,
        trigger='date',
        name=str(user_id),
        kwargs={
            'apscheduler': apscheduler,
            'bot': bot,
            'user_id': user_id,
            'text': text,
            'message': message
        }
    )