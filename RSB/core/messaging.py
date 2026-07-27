import logging

from telegram.ext import ContextTypes
from telegram.constants import ParseMode

import RSB.config as io
from RSB.core.state import CATEGORIES

log = logging.getLogger(__name__)


async def save_io(update, context):
    io.save_categories(CATEGORIES)


async def send_message(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    text: str,
    reply_markup=None,
    delete_message: bool = False,
    delete_markup: bool = False
):
    sent = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=reply_markup
    )

    if delete_message:
        pending = context.user_data.setdefault("pending_message", [])
        pending.append(sent.message_id)
    if delete_markup:
        pending = context.user_data.setdefault("pending_markup", [])
        pending.append(sent.message_id)

    return sent


async def edit_message(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    message_id,
    text: str,
    reply_markup=None,
    delete_message: bool = False,
    delete_markup: bool = False
):
    sent = await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=reply_markup
    )

    if delete_message:
        pending = context.user_data.setdefault("pending_message", [])
        pending.append(sent.message_id)
    if delete_markup:
        pending = context.user_data.setdefault("pending_markup", [])
        pending.append(sent.message_id)

    return sent


async def pending_handler(update, context):
    chat_id = update.effective_chat.id
    pending_message = context.user_data.pop("pending_message", [])
    pending_markup = context.user_data.pop("pending_markup", [])

    for message_id in pending_message:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception as e:
            log.warning(f"Не удалось удалить сообщение {message_id}: {e}")

    for message_id in pending_markup:
        try:
            await context.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)
        except Exception as e:
            log.warning(f"Не удалось удалить сообщение {message_id}: {e}")