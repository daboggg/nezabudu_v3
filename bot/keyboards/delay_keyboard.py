import json

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.db_actions import get_delay_times


async def delay_kb(job_id: str, user_id: int) -> InlineKeyboardMarkup:
    delay_times = await get_delay_times(user_id)
    delay_times = json.loads(delay_times)

    # delay_times = '{"hours": [1, 3]}',
    ikb = InlineKeyboardBuilder()

    for time, vals in delay_times.items():
        for val in vals:
            ikb.button(text=f'+{val} {"час" if time == "hours" else "мин"}', callback_data=f'delay_remind:{job_id}:{time}:{val}')

    ikb.button(text=f'⏰ Установить', callback_data=f'reschedule_remind:{job_id}')
    ikb.button(text=f'✔️ Выполнено', callback_data=f'done_remind:{job_id}')

    return ikb.adjust(3).as_markup()