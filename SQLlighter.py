# -*- coding: utf-8 -*-
import psycopg2
import urllib.parse as urlparse
import xmlparser


class SQLlighter:

    def __init__(self, database):

        url = urlparse.urlparse(database)

        self.connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        # self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()


    def check_user(self, user_id):
        """ Проверяем, есть ли пользователь с таким id в базе """
        with self.connection:
            self.cursor.execute('SELECT * FROM users WHERE id = %s;', (user_id,))

            data = self.cursor.fetchone()

            if data is None:
                return False
            else:
                return True

    def check_group(self, group_id):
        """ Проверяем, есть ли группа с таким id в базе """
        with self.connection:
            data = self.cursor.execute('SELECT * FROM users WHERE group_id = %s;', (group_id,)).fetchone()
            if data is None:
                return False
            else:
                return True

    def insert_schedule(self, user_id, group_id):
        schedule_for_week = xmlparser.getschedule(group_id)
        with self.connection:
            self.cursor.execute("INSERT INTO users VALUES (%s, %s,"
                                " %s, %s, %s, %s,"
                                " %s, %s, %s);", (user_id, group_id, *schedule_for_week))
            self.connection.commit()

    def update_schedule(self, user_id, group_id):
        schedule_for_week = xmlparser.getschedule(group_id)
        with self.connection:
            self.cursor.execute("UPDATE users SET group_id = %s, monday = %s,"
                                "tuesday = %s, wednesday = %s,"
                                " thursday = %s, friday = %s, saturday = %s, sunday = %s WHERE id = %s;", (group_id, *schedule_for_week, user_id))
            self.connection.commit()


    def update_schedule_by_group(self, group_id):
        schedule_for_week = xmlparser.getschedule(group_id)
        with self.connection:
            self.cursor.execute("UPDATE users SET monday = %s,"
                                "tuesday = %s, wednesday = %s,"
                                " thursday = %s, friday = %s, saturday = %s, sunday = %s WHERE group_id = %s;", (*schedule_for_week, group_id))
            self.connection.commit()

    def get_schedule(self, user_id, dayweek):
        dayweeks = {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'saturday', 6:'sunday'}
        with self.connection:
            self.cursor.execute("SELECT {} FROM users WHERE id = %s;".format(dayweeks[dayweek]), (user_id,))
            t = self.cursor.fetchall()
            return t


    def close(self):
        self.connection.close()