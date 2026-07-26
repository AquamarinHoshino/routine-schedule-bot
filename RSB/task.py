import logging


log = logging.getLogger(__name__)

class Task:
    def __init__(self, name, action, additional):
        self.name = name
        self.action = action
        self.additional = additional
        self.complete = False

    def __str__(self):
        return f"{self.name} {self.action} {self.additional} {self.complete}"
    
    def __repr__(self):
        return f"Task({self.name}, {self.action}, {self.additional}, {self.complete})"

    def Toggle(self):
        self.complete = not self.complete
        log.info(f'task {self.name} has toggled to {self.complete}')