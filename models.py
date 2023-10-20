from database import UserDatabase
import sqlite3

class User(UserDatabase):

    def __init__(self, username) -> None:
        self.username = username
        self.user_id = ""
        self.conn = sqlite3.connect("user_data.db", check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_task(self, taskname, description):
        user_id = self.get_user_id(self.username)
        self.create_task_db(user_id, taskname, description)

    def get_tasks(self):
        user_id = self.get_user_id(self.username)
        tasks = self.get_tasks_db(user_id)
        return tasks

    def delete_task(self, taskname):
        user_id = self.get_user_id(self.username)
        if user_id is not None:
            self.delete_task_db(taskname, user_id)
