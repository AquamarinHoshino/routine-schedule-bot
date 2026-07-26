import datetime as dt
import csv
import logging
import os
from RSB.Task import Task


log = logging.getLogger(__name__)
WEEKDAY_DICT = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье"
}

class Category:
    def __init__(self, public_name, file_name, size):
        log.info(f"category {public_name} initializing started")

        if size not in (1, 2):
            raise ValueError("size может быть только 1 или 2")
        
        self.public_name = public_name
        self.file_name = file_name
        self.size = size

        self._ensure_file_exists()
        self.tasks = self._read_csv()

        log.info(f"category {public_name} initializing completed succesfully")
    
    def __len__(self):
        return self.size
    
    def _default_csv_path(self) -> str:
        return f"default{self.size}.csv"
    
    def _ensure_file_exists(self):
        if '.csv' not in self.file_name:
            log.warning(f"file {self.file_name} is not a .csv file, filename was edited")
            self.file_name += '.csv'
        if not os.path.exists(self.file_name):
            log.error(f"file {self.file_name}.csv is not exist in project directory")
            with open(self.file_name, "w", newline="", encoding="utf-8") as f:
                f.write("day;action;additional\n")

    def _make_task_name(self, day: int) -> str:
        if self.size == 1:
            return f"{self.public_name}_{WEEKDAY_DICT[day%7]}"
        return f"{self.public_name}_{WEEKDAY_DICT[day%7]}{day//7}"

    def _read_csv(self) -> list:
        tasks: list = [None] * (7 * self.size)
        with open(self.file_name, 'r', encoding='utf-8') as file:
            arr = list(csv.DictReader(file, delimiter=';'))
            for row in arr:
                day = int(row["day"])
                action = (row.get("action") or "").strip()
                additional = (row.get("additional") or "").strip()
                tasks[day] = Task(self._make_task_name(day), action, additional)
            
        for day in range(7*self.size):
            if tasks[day] is None:
                log.warning(f"slot {day} in {self.file_name} is not exist")
                tasks[day] = Task(self._make_task_name(day), "", "")
        
        return tasks

    def _week_index_today(self) -> int:
        day_of_year = dt.datetime.now().timetuple().tm_yday
        return day_of_year % 2

    def today(self) -> Task:
        weekday = dt.date.today().weekday()
        if self.size == 1:
            idx = weekday
        else:
            idx = weekday + 7 * self._week_index_today()
        return self.tasks[idx]
    
    def save(self):
        with open(self.file_name, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["day", "action", "additional"])
            for day in range(7*self.size):
                task = self.tasks[day]
                writer.writerow([day, task.action, task.additional])

    def delete(self):
        os.remove(self.file_name)

    def get_task(self, day: int) -> Task:
        return self.tasks[day%14]

    def to_dict(self) -> dict:
        return {
            "public_name": self.public_name,
            "file_name": self.file_name,
            "size": self.size,
        }
 
    def create_task(self, day: int, action: str, additional: str = "", save: bool = True):
        day = day%14
        self.tasks[day] = Task(self._make_task_name(day), action, additional)
        if save:
            self.save()

    def edit_task(self, day: int, action: str = ';', additional: str = ';', save: bool = True):
        task = self.tasks[day%14]
        if action != ';':
            task.action = action
        if additional != ';':
            task.additional = additional
        if save:
            self.save()

    def toggle_task(self, day: int):
        self.tasks[day%14].Toggle()

    def __repr__(self):
        return f"Category({self.public_name!r}, {self.file_name!r}, size={self.size})"