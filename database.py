import sqlite3

class UserDatabase:
    def __init__(self, db_name='user_data.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
       
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                taskname TEXT NOT NULL,
                description TEXT,
                state TEXT DEFAULT 'Pending',
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        self.conn.commit()

    def register_user(self, username, password):
        self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        self.conn.commit()

    def check_username_exists(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone() is not None
    
    def create_task_db(self, user_id, taskname, description):
        self.cursor.execute('INSERT INTO tasks (user_id, taskname, description) VALUES (?, ?, ?)', (user_id, taskname, description))
        self.conn.commit()

    def get_tasks_db(self, user_id):
        self.cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()
    
    def update_task_db(self, taskname, choice, user_id):
        task_id = self.get_task_id_by_name(taskname, user_id)
        if task_id is not None:
            if choice == "1": 
                new_value = input("New taskname: ")
                self.cursor.execute('UPDATE tasks SET taskname=? WHERE id=?', (new_value, task_id))
            elif choice == "2": 
                new_value = input("New description: ")
                self.cursor.execute('UPDATE tasks SET description=? WHERE id=?', (new_value, task_id))
            elif choice == "3": 
                new_value = input(""" Select an option
1 - Pending
2 - On going
3 - Completed
   """)
            if new_value == "1":
                new_value = "Pending"
            elif new_value == "2":
                new_value = "On going"
            elif new_value == "3":
                new_value = "Completed"

                self.cursor.execute('UPDATE tasks SET state=? WHERE id=?', (new_value, task_id))
            self.conn.commit()

    def delete_task_db(self, taskname, user_id):
        task_id = self.get_task_id_by_name(taskname, user_id)
        if task_id is not None:
            self.cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
            self.conn.commit()

    def get_user_id(self, username):
        self.cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = self.cursor.fetchone()
        if user_id:
            return user_id[0]
        else:
            return None 
        
    def get_task_id_by_name(self, taskname, user_id):
        self.cursor.execute('SELECT id FROM tasks WHERE taskname = ? AND user_id = ?', (taskname, user_id))
        task_id = self.cursor.fetchone()
        if task_id:
            return task_id[0] 
        else:
            return None  

    def close_connection(self):
        self.conn.close()

    def __del__(self):
        self.close_connection()
