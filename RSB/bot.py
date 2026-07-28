import logging

from telegram import Update
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          TypeHandler, MessageHandler, filters)

from RSB.core.state import BOT_TOKEN
from RSB.core.security import restrict_access
from RSB.core.messaging import save_io, pending_handler

from RSB.handlers.basic import start_cmd, report_cmd
from RSB.handlers.select import select_cmd, select_task
from RSB.handlers.delete import delete_cmd, delete_cat
from RSB.handlers.add import build_add_conversation_handler
from RSB.handlers.remind import schedule_messages
from RSB.handlers.timezone import build_timezone_conversation_handler
from RSB.handlers.times import build_times_conversation_handler

log = logging.getLogger(__name__)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Блокиратор доступа — раньше всех остальных групп
    app.add_handler(MessageHandler(filters.ALL, restrict_access), group=-5)
    app.add_handler(CallbackQueryHandler(restrict_access), group=-5)

    # Базовые команды
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("report", report_cmd))
    app.add_handler(CommandHandler("select", select_cmd))
    app.add_handler(CommandHandler("delete", delete_cmd))

    # Коллбэки инлайн-кнопок
    app.add_handler(CallbackQueryHandler(select_task, pattern=r"^task_\d+$"), group=10)
    app.add_handler(CallbackQueryHandler(delete_cat, pattern=r"^del_\d+$"), group=10)

    # FSM добавления категории
    app.add_handler(build_add_conversation_handler(), group=10)

    # Напоминания
    schedule_messages(app)
    app.add_handler(build_times_conversation_handler(), group=10)
    app.add_handler(build_timezone_conversation_handler(), group=10)

    # Автоочистка pending-сообщений и автосейв категорий
    app.add_handler(TypeHandler(Update, pending_handler), group=-4)
    app.add_handler(CallbackQueryHandler(save_io), group=15)

    app.run_polling()


if __name__ == "__main__":
    main()