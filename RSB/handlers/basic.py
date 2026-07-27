from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from RSB.core.texts import get_active_tasks, get_all_tasks, all_cmds


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    active_tasks = get_active_tasks()
    text = "✋ *Привет\\! Вот твои дела на сегодня:*\n\n" + active_tasks[0] + active_tasks[1]
    await update.effective_message.reply_text(text, ParseMode.MARKDOWN_V2)
    await update.effective_message.reply_text(all_cmds(), ParseMode.MARKDOWN_V2)


async def report_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = get_all_tasks()
    text = "📄 *Отчёт по всем делам на сегодня:*\n\n" + tasks[0] + tasks[1]
    await update.effective_message.reply_text(text, ParseMode.MARKDOWN_V2)