from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (Application, ContextTypes, CommandHandler, 
                          MessageHandler, CallbackQueryHandler, filters,
                          ApplicationHandlerStop, TypeHandler, ConversationHandler)
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
import logging
import RSB.config as io


log = logging.getLogger(__name__)

BOT_TOKEN = io.BOT_TOKEN
USER_ID = io.USER_ID
CATEGORIES = io.load_categories()

SMILE_DICT = {
    True: "✅",
    False: "❌"
}

# Автосейв

async def save_io(update, context):
    io.save_categories(CATEGORIES)

# Отправка одноразок

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

# Блокиратор

async def restrict_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != USER_ID:
        log.info(f"unauthorized access by {user_id} {update.effective_user.link}")
        raise ApplicationHandlerStop

# Раскладки кнопок

def get_select_markup():
    vert = []
    tasks = get_all_tasks()[0].replace("\\", '').split("\n")
    j = 0
    for i in tasks:
        if i != "":
            vert.append([InlineKeyboardButton(i, callback_data=f"task_{j}")])
        j += 1
    return InlineKeyboardMarkup(vert)

def get_categories_markup():
    vert = []
    cats = get_all_categories().split("\n")
    j = 0
    for i in cats:
        if i != "":
            vert.append([InlineKeyboardButton(i, callback_data=f"del_{j}")])
        j += 1
    return InlineKeyboardMarkup(vert)

# Генераторы текста

def get_active_tasks():
    tasks = io.get_today_tasks(CATEGORIES, False)
    text1 = ""
    n = 0
    for task in tasks:
        if not task.complete:
            n += 1
            text1 += f"{SMILE_DICT[False]} {escape_markdown(task.name)} {escape_markdown(task.action)}\n"
    if n == 0:
        text2 = "\n🥰*На сегодня всё выполнено\\!*"
    else:
        text2 = f"\n😡У тебя ещё целых {n} задач\\! Немедленно займись ими"
    return (text1, text2)

def get_all_tasks():
    tasks = io.get_today_tasks(CATEGORIES, False)
    text1 = ""
    n = 0
    nn = len(tasks)
    for task in tasks:
        text1 += f"{SMILE_DICT[task.complete]} {escape_markdown(task.name)} {escape_markdown(task.action)} \\- {escape_markdown(task.additional)}\n"
        if task.complete:
            n += 1
    text0 = f"\nВыполнено {escape_markdown(str(int((n/nn if nn != 0 else 0)*100)), version=2)}% или {n}/{nn} задач\\!"
    if n == nn:
        text2 = text0 + f"\n🎉 *Это ещё один твой продуктивный день\\! Молодец\\!* 🎉"
    else:
        text2 = text0 + f"\n❗️ *Ещё не повод расслабляться\\!* ❗️"
    return (text1, text2)

def get_all_categories():
    tasks = [i.public_name for i in CATEGORIES]
    return '\n'.join(tasks)

def all_cmds():
    return "*Команды бота:*\n\n" \
    "/start \\- вывести это сообщение ещё раз\n" \
    "/report \\- вывод *всех задач* на сегодня\n" \
    "/select \\- назначить задачу выполненной\n" \
    "/delete \\- удалить категорию задач\n" \
    "/add \\- добавить категорию задач"

# Обработчики команд

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    active_tasks = get_active_tasks()
    text = "✋ *Привет\\! Вот твои дела на сегодня:*\n\n" + active_tasks[0] + active_tasks[1]
    await update.effective_message.reply_text(text, ParseMode.MARKDOWN_V2)
    await update.effective_message.reply_text(all_cmds(), ParseMode.MARKDOWN_V2)

async def report_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = get_all_tasks()
    text = "📄 *Отчёт по всем делам на сегодня:*\n\n" + tasks[0] + tasks[1]
    await update.effective_message.reply_text(text, ParseMode.MARKDOWN_V2)

async def select_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = get_all_tasks()
    text = "📝 *Режим выполнения:*\n\n" + tasks[0]
    await send_message(context, update.effective_chat.id, text, get_select_markup(), delete_markup=True)

async def delete_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🗑 *Режим удаления:*\n\n" + get_all_categories()
    await send_message(context, update.effective_chat.id, text, get_categories_markup(), delete_markup=True)

async def add_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Введите public\\_name категории"
    await update.effective_message.reply_text(text, ParseMode.MARKDOWN_V2)
    return 0

# Обработчики CallBack'ов

async def select_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    CATEGORIES[int(update.callback_query.data.split("_")[1])].today().Toggle()

    tasks = get_all_tasks()
    text = "📝 *Режим выполнения:*\n\n" + tasks[0]
    await edit_message(context, update.effective_chat.id, update.effective_message.id, text, reply_markup=get_select_markup(), delete_markup=True)

async def delete_cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    CATEGORIES.pop(int(update.callback_query.data.split("_")[1])).delete()

    text = "🗑 *Режим удаления:*\n\n" + get_all_categories()
    await edit_message(context, update.effective_chat.id, update.effective_message.id, text, reply_markup=get_categories_markup(), delete_markup=True)

# FSM для Edit

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

# Main

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, restrict_access), group=-5)
    app.add_handler(CallbackQueryHandler(restrict_access), group=-5)

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("report", report_cmd))
    app.add_handler(CommandHandler("select", select_cmd))
    app.add_handler(CommandHandler("delete", delete_cmd))

    app.add_handler(CallbackQueryHandler(select_task, pattern=r"^task_\d+$"), group=10)
    app.add_handler(CallbackQueryHandler(delete_cat, pattern=r"^del_\d+$"), group=10)

    add_handler = ConversationHandler(
        [CommandHandler("add", add_cmd)],
        {
            0: [MessageHandler(filters.ALL, add_public_name)],
            1: [MessageHandler(filters.ALL, add_file_name)],
            2: [MessageHandler(filters.ALL, add_size)],
            3: [MessageHandler(filters.ALL, add_data)]
        },
        [TypeHandler(Update, start_cmd)]
    )

    app.add_handler(add_handler, group=10)

    app.add_handler(TypeHandler(Update, pending_handler), group=-4)
    app.add_handler(CallbackQueryHandler(save_io), group=15)

    app.run_polling()
