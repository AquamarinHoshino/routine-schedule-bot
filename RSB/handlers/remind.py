from telegram.ext import Application, ContextTypes
from telegram.constants import ParseMode

from RSB.core.state import USER_ID, CATEGORIES, get_schedule_times
from RSB.core.texts import get_remind

from RSB.config import get_today_tasks

import logging


logger = logging.getLogger(__name__)

current_jobs = []


async def send_scheduled_message(context: ContextTypes.DEFAULT_TYPE):
    if len(get_today_tasks(CATEGORIES, True)) == 0:
        return
    try:
        await context.bot.send_message(
            chat_id=USER_ID,
            text=get_remind(),
            parse_mode=ParseMode.MARKDOWN_V2
        )
        logger.info(f"Сообщение отправлено пользователю {USER_ID}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")


def clear_jobs(name: str, application: Application):
    current_job = application.job_queue.get_jobs_by_name(name)
    if not current_job:
        return False
    for job in current_job:
        job.schedule_removal()


def schedule_messages(application: Application):
    for i in current_jobs:
        clear_jobs(i, application)
    current_jobs.clear()

    for schedule_time in get_schedule_times():
        current_job_name = f"scheduled_{schedule_time.strftime('%H:%M')}"
        current_jobs.append(current_job_name)
        application.job_queue.run_daily(
            send_scheduled_message,
            time=schedule_time,
            days=(0, 1, 2, 3, 4, 5, 6),
            name=current_job_name,
            user_id=USER_ID
        )
        logger.info(f"Запланирована отправка на {schedule_time.strftime('%H:%M')}")