import os
import json
from RSB.Category import Category
import logging


log = logging.getLogger(__name__)
SETTINGS_FILE = os.path.join(
    os.path.abspath(
        os.path.dirname(os.path.dirname(__name__))),
          'settings.json')

def load_settings() -> tuple[str, int, list[Category]]:
    if not os.path.isfile(SETTINGS_FILE):
        log.warning(f"settings file {SETTINGS_FILE} is not exist")
        return ("None", "None", [])
    else:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as file:
            try:
                file_json = json.load(file)
                bot_token = file_json.get('bot_token')
                user_id = file_json.get('user_id')
                arr = file_json.get('categories')
                return (bot_token, user_id, [Category(i['public_name'], i['file_name'], i['size']) for i in arr])
            except json.decoder.JSONDecodeError:
                log.warning(f"settings file {SETTINGS_FILE} is corrupted")
                os.remove(SETTINGS_FILE)
                return ("None", "None", [])

def save_categories(bot_token: str, user_id: int, categories: list):
    data = {"bot_token": bot_token, "user_id": user_id, "categories": [c.to_dict() for c in categories]}
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)

def create_category(categories: list, public_name: str, file_name: str, size: int) -> Category:
    file_name = categories_dir(file_name)
    category = Category(public_name, file_name, size)
    categories.append(category)
    return category

def get_today_tasks(arr: list[Category], only_actives: bool = False):
    res = []
    for i in arr:
        task = i.today()
        if (only_actives and not task.complete) or not only_actives:
            res.append(task)
    return res

def categories_dir(file_name: str) -> str:
    return os.path.join("categories", file_name)