from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Format

from bot.actions import get_reminder, add_reminder
from bot.state_groups import MainDialog
from utils.reminder_info import get_reminder_info


async def getter_set_reminder(dialog_manager: DialogManager, **kwargs):
    if dialog_manager.dialog_data.get("reminder"):

        reminder_info = get_reminder_info(dialog_manager)

        return {"text": reminder_info}

    return {
        "text": "пожалуйста введите время и текст напоминания",
    }


async def set_reminder(event, widget, dialog_manager: DialogManager, *_):
    dialog_manager.dialog_data.clear()
    try:
        reminder = await get_reminder(event)
        dialog_manager.dialog_data["reminder"] = reminder
        await add_reminder(dialog_manager)
    except Exception as e:
        print(e)




# диалог список напоминаний
main_dialog = Dialog(
    Window(
        Format('{text}'),
        MessageInput(set_reminder),
        # Back(Const("Назад")),
        # Button(Const("Удалить"),id='delete_reminder', on_click=on_delete_selected),
        state=MainDialog.set_reminder,
        getter=getter_set_reminder,
    ),
)