from aiogram.types import User
import psycopg2
import psycopg2.extras
import datetime
from os import listdir

class PostgreSQLDatabase:
    def __init__(self, database_url: str):
        self.conn = psycopg2.connect(dsn=database_url, keepalives=1, keepalives_idle=300, keepalives_interval=60, keepalives_count=30)
        self.curs = self.conn.cursor()
        self.curd = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.conn.autocommit = True

    def createTables(self):
        self.curs.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id int8 PRIMARY KEY NOT NULL,
                username TEXT NOT NULL,
                classroom TEXT,
                locale TEXT,
                join_time TIMESTAMP
                )''')

        class_list = []
        for i in range(6, 12):
            for n in ["А", "Б", "В"]:
                class_list.append(str(i) + '-' + n)
        
        self.curs.execute('''
            CREATE TABLE IF NOT EXISTS timetable (
                classroom TEXT PRIMARY KEY NOT NULL UNIQUE,
                Monday TEXT DEFAULT '{temp}',
                Tuesday TEXT DEFAULT '{temp}',
                Wednesday TEXT DEFAULT '{temp}',
                Thursday TEXT DEFAULT '{temp}',
                Friday TEXT DEFAULT '{temp}',
                Saturday TEXT DEFAULT '{temp}')'''.format(temp="S/T|S/T"))

        for c in class_list:
            self.curs.execute('''INSERT INTO timetable (classroom) VALUES(%s) ON CONFLICT (classroom) DO NOTHING''', (c,))

        self.curs.execute('''
            CREATE TABLE IF NOT EXISTS time (
                abb BOOLEAN,
                first TEXT,
                second TEXT,
                third TEXT,
                forth TEXT,
                fifth TEXT,
                sixth TEXT,
                seventh TEXT,
                eighth TEXT
            )''')

    def addUser(self, user: User):
        if not user.username:
            user.username = user.full_name

        if user.language_code not in listdir("locale"):
            user.language_code = "ru_RU"

        self.curs.execute('''INSERT INTO "users" 
            ("id", "username", "locale", "join_time") 
            VALUES(%s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET username = '{username}';'''.format(username=user.username), 
            (user.id, user.username, user.language_code, datetime.datetime.now()))

    def getUser(self, user: User):
        self.curd.execute('''SELECT * FROM users WHERE id = %s''', (user.id,))
        result = self.curd.fetchone()

        return result


    def setUserClass(self, user: User, data: str):
        self.curs.execute('''UPDATE users SET classroom = %s WHERE id = %s''', (data, user.id))


    def setUserLocale(self, user: User, data: str):
        self.curs.execute('''UPDATE users SET locale = %s WHERE id = %s''', (data, user.id))


    def getTime(self, abb):
        self.curs.execute('''SELECT * FROM time WHERE abb = %s''', (abb,))
        result = self.curs.fetchone()

        return result[1:]
    
    def setTimetable(self, classroom: str, weekday: str):
        return


    def getTimetable(self, user: User, weekday: str) -> list[list[str]]:
        classroom = self.getUser(user)["classroom"]
        if weekday == "sunday":
            return
        
        self.curd.execute('''SELECT * FROM timetable WHERE classroom = %s''', (classroom, ))

        result = self.curd.fetchone()
        result = result[weekday]
        result = result.split('|')

        for r in result:
            if r == result[0]:
                result = []

            result.append(r.split('/'))
        
        return result
