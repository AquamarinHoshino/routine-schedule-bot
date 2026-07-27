from random import randint

from telegram.helpers import escape_markdown

import RSB.config as io
from RSB.core.state import CATEGORIES, SMILE_DICT
from RSB.core.state import (RESOURCES_COMPLETE, RESOURCES_NOT_COMPLETE, RESOURCES_COMPLETE_N,
                        RESOURCES_NOT_COMPLETE_N, RESOURCES_REMIND)


def get_text(name: str, n: int = -1):
    file = io.load_resource(name)
    rnd = randint(0, len(file)-1)
    return "\n" + (file[rnd] if n == -1 else file[rnd].format(n))


def get_active_tasks():
    tasks = io.get_today_tasks(CATEGORIES, False)
    text1 = ""
    n = 0
    for task in tasks:
        if not task.complete:
            n += 1
            text1 += f"{SMILE_DICT[False]} {escape_markdown(task.name)} {escape_markdown(task.action)}\n"
    if n == 0:
        text2 = get_text(RESOURCES_COMPLETE)
    else:
        text2 = get_text(RESOURCES_NOT_COMPLETE_N, n)
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
        text2 = text0 + get_text(RESOURCES_COMPLETE_N, n)
    else:
        text2 = text0 + get_text(RESOURCES_NOT_COMPLETE)
    return (text1, text2)


def get_all_categories():
    tasks = [i.public_name for i in CATEGORIES]
    return '\n'.join(tasks)


def get_remind():
    return get_text(RESOURCES_REMIND) + "\n" + ''.join(get_active_tasks())


def all_cmds():
    return "*Команды бота:*\n\n" \
    "/start \\- вывести это сообщение ещё раз\n" \
    "/report \\- вывод *всех задач* на сегодня\n" \
    "/select \\- назначить задачу выполненной\n" \
    "/delete \\- удалить категорию задач\n" \
    "/add \\- добавить категорию задач"