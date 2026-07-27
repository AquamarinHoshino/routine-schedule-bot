from telegram import Update
from telegram.ext import ContextTypes

from RSB.core.state import CATEGORIES
from RSB.core.texts import get_all_tasks
from RSB.core.keyboards import get_select_markup
from RSB.core.messaging import send_message, edit_message


async def select_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = get_all_tasks()
    text = "📝 *Режим выполнения:*\n\n" + tasks[0]
    await send_message(context, update.effective_chat.id, text, get_select_markup(), delete_markup=True)


async def select_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    CATEGORIES[int(update.callback_query.data.split("_")[1])].today().Toggle()

    tasks = get_all_tasks()
    text = "📝 *Режим выполнения:*\n\n" + tasks[0]
    await edit_message(context, update.effective_chat.id, update.effective_message.id, text, reply_markup=get_select_markup(), delete_markup=True)