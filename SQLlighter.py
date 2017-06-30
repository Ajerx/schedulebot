# -*- coding: utf-8 -*-
import sqlite3
import xmlparser


class SQLlighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()


    def check_user(self, user_id):
        """ Проверяем, есть ли пользователь с таким id в базе """
        with self.connection:
            data = self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            if data is None:
                return False
            else:
                return True

    def check_group(self, group_id):
        """ Проверяем, есть ли группа с таким id в базе """
        with self.connection:
            data = self.cursor.execute('SELECT * FROM users WHERE group_id = ?', (group_id,)).fetchone()
            if data is None:
                return False
            else:
                return True

    def insert_schedule(self, user_id, group_id):
        schedule_for_week = xmlparser.getschedule(group_id)
        with self.connection:
            self.cursor.execute("INSERT INTO users VALUES (?, ?,"
                                " ?, ?, ?, ?,"
                                " ?, ?, ?)", (user_id, group_id, *schedule_for_week))
            self.connection.commit()

    def update_schedule(self, user_id, group_id):
        schedule_for_week = xmlparser.getschedule(group_id)
        with self.connection:
            self.cursor.execute("UPDATE users SET group_id = ?, monday = ?,"
                                "tuesday = ?, wednesday = ?,"
                                " thursday = ?, friday = ?, saturday = ?, sunday = ? WHERE id = ?", (group_id, *schedule_for_week, user_id))
            self.connection.commit()


    def update_schedule_by_group(self, group_id):
        schedule_for_week = xmlparser.getschedule(group_id)
        with self.connection:
            self.cursor.execute("UPDATE users SET monday = ?,"
                                "tuesday = ?, wednesday = ?,"
                                " thursday = ?, friday = ?, saturday = ?, sunday = ? WHERE group_id = ?", (*schedule_for_week, group_id))
            self.connection.commit()

    def get_schedule(self, user_id, dayweek):
        dayweeks = {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'saturday', 6:'sunday'}
        with self.connection:
            self.cursor.execute("SELECT {} FROM users WHERE id = ?".format(dayweeks[dayweek]), (user_id,))
            t = self.cursor.fetchall()
            return t


    def close(self):
        self.connection.close()