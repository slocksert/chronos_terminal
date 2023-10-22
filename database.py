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

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS finances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                budget INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                expense_name TEXT,
                expense_value INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        self.conn.commit()

    #tasks    
    def create_task(self, user_id, taskname, description):
        self.cursor.execute('INSERT INTO tasks (user_id, taskname, description) VALUES (?, ?, ?)', (user_id, taskname, description))
        self.conn.commit()

    def get_tasks(self, user_id):
        self.cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()
    
    def update_task(self, taskname, choice, user_id):
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

    def delete_task(self, taskname, user_id):
        task_id = self.get_task_id_by_name(taskname, user_id)
        if task_id is not None:
            self.cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
            self.conn.commit()
        
    def get_task_id_by_name(self, taskname, user_id):
        self.cursor.execute('SELECT id FROM tasks WHERE taskname = ? AND user_id = ?', (taskname, user_id))
        task_id = self.cursor.fetchone()
        if task_id:
            return task_id[0] 
        else:
            return None  

    # Finances
    def set_budget(self, user_id, budget):
        self.cursor.execute('INSERT OR REPLACE INTO finances (user_id, budget) VALUES (?, ?)', (user_id, budget))
        self.conn.commit()

    def add_expense(self, user_id, expense_value, expense_name):
        self.cursor.execute('INSERT INTO expenses (user_id, expense_name, expense_value) VALUES (?, ?, ?)', (user_id, expense_name, expense_value))
        self.conn.commit()

    def remove_expense(self, user_id, expense_name):
        expense_id = self.get_expenses_by_name(expense_name=expense_name, user_id=user_id)[0]
        if expense_id is not None:
            self.cursor.execute('DELETE FROM expenses WHERE id=?', (expense_id,))
            self.conn.commit()
    
    def update_expense(self, user_id, expense_name, choice):
        expense_id = self.get_expenses_by_name(expense_name=expense_name, user_id=user_id)[0]
        if expense_id is not None:
            if choice == "1": 
                new_value = input("New expense name: ")
                self.cursor.execute('UPDATE expenses SET expense_name=? WHERE id=?', (new_value, expense_id))
            elif choice == "2": 
                new_value = input("New expense value: ")
                self.cursor.execute('UPDATE expenses SET expense_value=? WHERE id=?', (new_value, expense_id))

    def get_total_expenses(self, user_id):
        self.cursor.execute('SELECT expense_value FROM expenses WHERE user_id=?', (user_id,))
        total_expenses = self.cursor.fetchall()
        sum_expenses = []

        if total_expenses:
            for expenses in total_expenses:
                sum_expenses.append(expenses[0])
            return sum_expenses
        else:
            return 0

    def get_budget(self, user_id):
        self.cursor.execute('SELECT budget FROM finances WHERE user_id=?', (user_id,))
        budget = self.cursor.fetchone()
        if budget:
            return budget[0]
        else:
            return 0

    def get_finances(self, user_id):
        self.cursor.execute('SELECT * FROM expenses WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()
    
    def get_expenses_by_name(self, user_id, expense_name):
        self.cursor.execute('SELECT id FROM expenses WHERE expense_name = ? AND user_id = ?', (expense_name, user_id))
        return self.cursor.fetchone()

    #general
    def get_user_id(self, username):
        self.cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = self.cursor.fetchone()
        if user_id:
            return user_id[0]
        else:
            return None 
        
    def register_user(self, username, password):
        self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        self.conn.commit()

    def check_username_exists(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone() is not None

    def close_connection(self):
        self.conn.close()

    def __del__(self):
        self.close_connection()
