from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def delay_kb(job_id: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()

    ikb.button(text=f'+1 час', callback_data=f'delay_remind:{job_id}:1')
    ikb.button(text=f'+3 часа', callback_data=f'delay_remind:{job_id}:3')
    ikb.button(text=f'⏰ Установить', callback_data=f'reschedule_remind:{job_id}')
    ikb.button(text=f'✔️ Выполнено', callback_data=f'done_remind:{job_id}')

    return ikb.adjust(2).as_markup()