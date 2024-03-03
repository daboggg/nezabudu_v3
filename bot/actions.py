from aiogram.types import Message

from parser_v3.parse import parse
from parser_v3.reminder import Reminder
from utils.converter import conv_voice


async def get_reminder(event: Message)-> Reminder:
    if event.text:
        return parse(event.text)
    elif event.voice:
        text = await conv_voice(event, event.bot)
        return parse(text)