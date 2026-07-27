from telegram import Update
from telegram.ext import ContextTypes

from RSB.core.state import CATEGORIES
from RSB.core.texts import get_all_categories
from RSB.core.keyboards import get_categories_markup
from RSB.core.messaging import send_message, edit_message


async def delete_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🗑 *Режим удаления:*\n\n" + get_all_categories()
    await send_message(context, update.effective_chat.id, text, get_categories_markup(), delete_markup=True)


async def delete_cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    CATEGORIES.pop(int(update.callback_query.data.split("_")[1])).delete()

    text = "🗑 *Режим удаления:*\n\n" + get_all_categories()
    await edit_message(context, update.effective_chat.id, update.effective_message.id, text, reply_markup=get_categories_markup(), delete_markup=True)