from telegram import Update
from telegram.ext import (ContextTypes, CommandHandler, MessageHandler,
                          filters, TypeHandler, ConversationHandler)
from telegram.constants import ParseMode

from RSB.core.texts import all_cmds
from RSB.core.state import set_times
from RSB.handlers.basic import start_cmd
from RSB.handlers.remind import schedule_messages


async def times_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Введите время когда вам будет высылаться напоминание, с каждой строчки новое значение формата ЧАСЫ МИНУТЫ \\(пример: 12 0\\)"
    await update.effective_message.reply_text(text, ParseMode.MARKDOWN_V2)
    return 0


async def set_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    arr = [[int(i.split(' ')[0]), int(i.split(' ')[1])] for i in update.effective_message.text.split('\n')]
    set_times(times=arr)
    schedule_messages(context.application)

    await update.effective_message.reply_text(f"✅ Время напоминания успешно обновлены!")
    await update.effective_message.reply_text(all_cmds(), ParseMode.MARKDOWN_V2)
    
    return -1


def build_times_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        [CommandHandler("times", times_cmd)],
        {
            0: [MessageHandler(filters.ALL, set_time)]
        },
        [TypeHandler(Update, start_cmd)]
    )