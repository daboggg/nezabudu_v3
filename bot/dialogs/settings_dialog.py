import json
import operator

from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.widgets.kbd import Radio, ManagedRadio, SwitchTo, Column, Multiselect, Back
from aiogram_dialog.widgets.text import Format, Const

from bot.state_groups import SettingsReminders
from db.db_actions import set_auto_delay_time, get_auto_delay_time


async def get_data(**kwargs):
    fruits = [
        ("Apple", '1'),
        ("Pear", '2'),
        ("Orange", '3'),
        ("Banana", '4'),
    ]
    return {
        "fruits": fruits,
        "count": len(fruits),
    }


async def on_state_changed_auto_delay(event: Message, select: ManagedRadio, dialog_manager: DialogManager, data):
    await set_auto_delay_time(event.from_user.id, {"minutes": int(data)})


async def dialog_on_start(_, manager: ManagerImpl):
    res = await get_auto_delay_time(manager.event.from_user.id)
    auto_delay_time: dict = json.loads(res)
    radio: ManagedRadio = manager.find('a_delay')
    await radio.set_checked(auto_delay_time.get("minutes"))


setting_dialog = Dialog(
    Window(
        Const("⚙️ выберите раздел"),
        Column(
            SwitchTo(Const("автоматическое откладывание"), state=SettingsReminders.select_auto_delay, id="auto_delay"),
            SwitchTo(Const("кнопки откладывания"), state=SettingsReminders.select_buttons_delay, id="button_delay"),
        ),
        state=SettingsReminders.select_setting
    ),
    Window(
        Const("Установите время, на которое напоминания будут автоматически откладываться."),
        Column(
            Radio(
                Format("🔘 {item[0]}"),
                Format("⚪️ {item[0]}"),
                id="a_delay",
                item_id_getter=operator.itemgetter(1),
                # item_id_getter=lambda x: x,
                items=[("5 минут", 5), ("10 минут", 10), ("15 минут", 15), ("20 минут", 20)],
                on_state_changed=on_state_changed_auto_delay
            ),
            Back(Const("назад"))
        ),
        getter=get_data,
        state=SettingsReminders.select_auto_delay
    ),
    Window(
        Const("UUUUUUUUUUUU"),
        Multiselect(
            Format("✓ {item[0]}"),
            Format("{item[0]}"),
            id="btn_delay",
            item_id_getter=operator.itemgetter(1),
            items="fruits",
            max_selected=1
        ),
        getter=get_data,
        state=SettingsReminders.select_buttons_delay
    ),
    on_start=dialog_on_start
)
