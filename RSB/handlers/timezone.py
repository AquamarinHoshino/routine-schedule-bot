from telegram import Update
from telegram.ext import (ContextTypes, CommandHandler, MessageHandler,
                          filters, TypeHandler, ConversationHandler)
from telegram.constants import ParseMode

from RSB.core.texts import all_cmds
from RSB.core.state import set_times
from RSB.handlers.basic import start_cmd
from RSB.handlers.remind import schedule_messages


async def tz_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Введите timedelta от UTC"
    await update.effective_message.reply_text(text, ParseMode.MARKDOWN_V2)
    return 0


async def set_tz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_times(tz=int(update.effective_message.text))
    schedule_messages(context.application)
    
    await update.effective_message.reply_text(f"✅ Timezone выставлен на UTC+{update.effective_message.text}!")
    await update.effective_message.reply_text(all_cmds(), ParseMode.MARKDOWN_V2)

    return -1


def build_timezone_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        [CommandHandler("tz", tz_cmd)],
        {
            0: [MessageHandler(filters.ALL, set_tz)]
        },
        [TypeHandler(Update, start_cmd)]
    )