import json
import logging

import apscheduler.events
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_helper import db_helper
from models import User, Task
from parser_v3.reminder import Reminder

logger = logging.getLogger(__name__)


# добавляет пользователя в бд
async def add_user_to_db(user_id: int, username: str, first_name: str, last_name: str):
    session = db_helper.get_scoped_session()
    user: User = (await session.execute(select(User).where(User.id == user_id))).scalar()

    if not user:
        user = User(
            id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            delay_times='''["('minutes', 10, '10 мин')"]''',
            auto_delay_time='{"minutes": 15}',
        )
        session.add(user)
        await session.commit()
    await session.close()


# добавить авто откладывание напоминания
async def set_auto_delay_time(user_id: int, auto_delay_time: dict):
    session = db_helper.get_session()
    user: User = await session.get(User, user_id)
    user.auto_delay_time = json.dumps(auto_delay_time)
    await session.commit()
    await session.close()



# получить авто откладывание напоминания
async def get_auto_delay_time(user_id: int):
    session = db_helper.get_session()
    user: User = await session.get(User, user_id)
    auto_delay_time = user.auto_delay_time
    await session.close()
    return auto_delay_time


# добавить откладывания напоминания
async def set_delay_times(user_id: int, delay_times: str):
    session = db_helper.get_session()
    user: User = await session.get(User, user_id)
    user.delay_times = delay_times
    await session.commit()
    await session.close()


# получить набор для кнопок откладывания напоминания
async def get_delay_times(user_id: int):
    session = db_helper.get_session()
    user: User = await session.get(User, user_id)
    delay_times = user.delay_times
    await session.close()
    return delay_times


# добавить задание в бд
async def add_remind_to_db(message:Message, state: FSMContext, job_id: int):
    session = db_helper.get_scoped_session()
    state_data = await state.get_data()
    reminder: Reminder = state_data.get("reminder")

    # если run_date присутствует в словаре, преобразуем datetime в строку
    if rd := reminder.params.get("run_date"):
        reminder.params["run_date"] = str(rd)

    remind = Task(
        id=job_id,
        params=json.dumps(reminder.params),
        user_id=message.from_user.id,
        text=reminder.message,
        period=reminder.period,
    )
    session.add(remind)
    await session.commit()
    await session.close()



# редактирование задания в бд
async def edit_task_to_db(state: FSMContext):
    session: AsyncSession = db_helper.get_scoped_session()
    state_data = await state.get_data()
    reminder:Reminder = state_data.get("reminder")

    params = reminder.params
    message = reminder.message
    period = reminder.period
    job_id = state_data.get("job_id")

    result = await session.execute(select(Task).where(Task.id == job_id))
    if remind := result.scalar():
        logger.info(f"получен job с id: {job_id}")
        if params:
            # если run_date присутствует в словаре, преобразуем datetime в строку
            if rd := params.get("run_date"):
                params["run_date"] = str(rd)
            remind.params = json.dumps(params)
        if message:
            remind.text = message
        if period:
            remind.period = period
        else:
            remind.period = None

        session.add(remind)
        logger.info(f"добавлен job с id: {job_id}")
        result = (remind.period, remind.text)
        await session.commit()
        await session.close()
        return result


# взять все задания из бд
async def get_tasks_from_db() -> list[Task]:
    session = db_helper.get_scoped_session()

    result: Result = await session.execute(select(Task))
    tasks = result.scalars().all()
    await session.close()

    return list(tasks)


# удалить задание из бд
async def delete_task_from_db(job: apscheduler.events.JobEvent):
    session: AsyncSession = db_helper.get_scoped_session()
    result = await session.execute(select(Task).where(Task.id == job.job_id))
    if task := result.scalar():
        logger.info(f"удален job с id: {job.job_id}")
        await session.delete(task)
    await session.commit()
    await session.close()


# взять задание из бд
async def get_task_from_db(job_id: int) -> Task:
    session = db_helper.get_scoped_session()
    result = await session.execute(select(Task).where(Task.id == job_id))
    logger.info(f"получен reminder с id: {job_id}")
    result = result.scalar()
    await session.close()
    return result


async def get_tasks_from_db_by_user_id(user_id: int) -> list[Task]:
    session = db_helper.get_scoped_session()

    result: Result = await session.execute(select(Task).where(Task.user_id == user_id))
    tasks = result.scalars().all()
    await session.close()

    return list(tasks)
