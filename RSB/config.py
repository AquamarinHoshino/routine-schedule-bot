import os
import json
from dotenv import load_dotenv
from RSB.category import Category
import logging
from pathlib import Path


log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
CATEGORIES_FILE = BASE_DIR / "categories.json"
CATEGORIES_DIR = BASE_DIR / "categories"

load_dotenv()
BOT_TOKEN: str = os.environ["BOT_TOKEN"]
USER_ID: int = int(os.environ["USER_ID"])


def load_categories() -> list[Category]:

    if not os.path.isfile(CATEGORIES_FILE):
        log.warning(f"categories file {CATEGORIES_FILE} is not exist")
        return []
    
    else:
        with open(CATEGORIES_FILE, 'r', encoding='utf-8') as file:

            try:
                file_json = json.load(file)
                arr = file_json.get('categories')
                return [Category(i['public_name'], os.path.join(*i['file_name']), i['size']) for i in arr]
            
            except json.decoder.JSONDecodeError:
                log.warning(f"settings file {CATEGORIES_FILE} is corrupted")
                os.remove(CATEGORIES_FILE)
                return []

def save_categories(categories: list) -> None:
    data = {"categories": [c.to_dict() for c in categories]}
    with open(CATEGORIES_FILE, "w", encoding="utf-8") as file:
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
    return str(CATEGORIES_DIR / file_name)