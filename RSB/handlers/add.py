from telegram import Update
from telegram.ext import (ContextTypes, CommandHandler, MessageHandler,
                          filters, TypeHandler, ConversationHandler)
from telegram.constants import ParseMode

import RSB.config as io
from RSB.core.state import CATEGORIES
from RSB.core.texts import all_cmds
from RSB.handlers.basic import start_cmd


async def add_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Введите public\\_name категории"
    await update.effective_message.reply_text(text, ParseMode.MARKDOWN_V2)
    return 0


async def add_public_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['public_name'] = update.effective_message.text
    text = "Введите file\\_name категории"
    await update.effective_message.reply_text(text, ParseMode.MARKDOWN_V2)
    return 1


async def add_file_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['file_name'] = update.effective_message.text
    text = "Введите size категории"
    await update.effective_message.reply_text(text, ParseMode.MARKDOWN_V2)
    return 2


async def add_size(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['size'] = update.effective_message.text
    text = f"Введите {7*int(update.effective_message.text)} строк по 3 элемента через пробел\n" \
        "day\\|action\\|additional"
    await update.effective_message.reply_text(text, ParseMode.MARKDOWN_V2)
    return 3


async def add_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cat = io.create_category(CATEGORIES, context.user_data['public_name'], context.user_data['file_name'], int(context.user_data['size']))
    io.save_categories(CATEGORIES)
    arr = update.effective_message.text.split("\n")
    for i in arr:
        task = i.split(" ")
        cat.create_task(int(task[0]), task[1], " ".join(task[2::]))
    await update.effective_message.reply_text(f"✅ Категория {context.user_data['public_name']} успешно добавлена!")
    await update.effective_message.reply_text(all_cmds(), ParseMode.MARKDOWN_V2)
    return -1


def build_add_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        [CommandHandler("add", add_cmd)],
        {
            0: [MessageHandler(filters.ALL, add_public_name)],
            1: [MessageHandler(filters.ALL, add_file_name)],
            2: [MessageHandler(filters.ALL, add_size)],
            3: [MessageHandler(filters.ALL, add_data)]
        },
        [TypeHandler(Update, start_cmd)]
    )