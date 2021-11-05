import sqlite3
from aiogram.types import User

class SQLite:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.curs = self.conn.cursor()
    
    def getTimetable(self, user: User, weekday: str):
        pass