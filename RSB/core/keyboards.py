from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from RSB.core.texts import get_all_tasks, get_all_categories


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