from telegram.ext import Application, ContextTypes
from telegram.constants import ParseMode

from RSB.core.state import USER_ID, SCHEDULE_TIMES, CATEGORIES
from RSB.core.texts import get_remind

from RSB.config import get_today_tasks

import logging


logger = logging.getLogger(__name__)


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


def schedule_messages(application: Application):
    for schedule_time in SCHEDULE_TIMES:
        application.job_queue.run_daily(
            send_scheduled_message,
            time=schedule_time,
            days=(0, 1, 2, 3, 4, 5, 6),
            name=f"scheduled_{schedule_time.strftime('%H:%M')}"
        )
        logger.info(f"Запланирована отправка на {schedule_time.strftime('%H:%M')}")