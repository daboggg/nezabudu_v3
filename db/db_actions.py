import json
import logging

import apscheduler.events
from aiogram.fsm.context import FSMContext
from apscheduler.job import Job
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_helper import db_helper

logger = logging.getLogger(__name__)


# добавить задание в бд
# async def add_remind_to_db(state: FSMContext, user_id: int) -> int:
#     session = db_helper.get_scoped_session()
#     state_data = await state.get_data()
#     remind = state_data.get("remind")
#     params = remind.get("params")
#     messages = remind.get("messages")
#
#     # если run_date присутствует в словаре, преобразуем datetime в строку
#     if rd := params.get("run_date"):
#         params["run_date"] = str(rd)
#
#     remind = Remind(
#         params=json.dumps(params),
#         chat_id=user_id,
#         text=messages.get('message'),
#         period=messages.get('period', None),
#     )
#     session.add(remind)
#     await session.flush()
#     remind_id = remind.id
#     await session.commit()
#     await session.close()
#
#     return remind_id
#
#
# # редактирование задания в бд
# async def edit_task_to_db(state: FSMContext, job: Job):
#     session: AsyncSession = db_helper.get_scoped_session()
#     state_data = await state.get_data()
#
#     params = state_data.get("params", None)
#     message = state_data.get("message", None)
#     period = state_data.get("period", None)
#
#     result = await session.execute(select(Remind).where(Remind.id == int(job.id)))
#     if remind := result.scalar():
#         logger.info(f"получен job с id: {job.id}")
#         if params:
#             # если run_date присутствует в словаре, преобразуем datetime в строку
#             if rd := params.get("run_date"):
#                 params["run_date"] = str(rd)
#             remind.params = json.dumps(params)
#         if message:
#             remind.text = message
#         if period:
#             remind.period = period
#         else:
#             remind.period = None
#
#         session.add(remind)
#         logger.info(f"добавлен job с id: {job.id}")
#         result = (remind.period, remind.text)
#         await session.commit()
#         await session.close()
#         return result
#
#
# # взять все задания из бд
# async def get_tasks_from_db() -> list[Remind]:
#     session = db_helper.get_scoped_session()
#
#     result: Result = await session.execute(select(Remind))
#     tasks = result.scalars().all()
#     await session.close()
#
#     return list(tasks)
#
#
# # удалить задание из бд
# async def delete_task_from_db(job: apscheduler.events.JobEvent):
#     session: AsyncSession = db_helper.get_scoped_session()
#     if job.job_id.isdigit():
#         result = await session.execute(select(Remind).where(Remind.id == int(job.job_id)))
#         if task := result.scalar():
#             logger.info(f"удален job с id: {job.job_id}")
#             await session.delete(task)
#         await session.commit()
#         await session.close()
#
#
# # взять задание из бд
# async def get_task_from_db(reminder_id: int) -> Remind:
#     session = db_helper.get_scoped_session()
#     result = await session.execute(select(Remind).where(Remind.id == reminder_id))
#     logger.info(f"получен reminder с id: {reminder_id}")
#     result = result.scalar()
#     await session.close()
#     return result
#
#
# async def get_tasks_from_db_by_user_id(user_id: int) -> list[Remind]:
#     session = db_helper.get_scoped_session()
#
#     result: Result = await session.execute(select(Remind).where(Remind.chat_id == user_id))
#     tasks = result.scalars().all()
#     await session.close()
#
#     return list(tasks)
