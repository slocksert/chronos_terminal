import getpass

from database import UserDatabase

def verify_if_user_exists(username):
    db = UserDatabase()

    if db.check_username_exists(username):
        return 1
    else:
        return 0
    
def register_user():
    db = UserDatabase()

    print("\nRegister Area")
    print(len("Register Area") * "_")

    username = input("Type the username you would like to use: ")
    password = getpass.getpass("Enter your password: ")

    user_boolean_value = verify_if_user_exists(username)

    if user_boolean_value == True:
        return False
    else:
        db.register_user(username=username, password=password)
        return True
    
def user_login():
    db = UserDatabase()
    
    print("\nLogin Area")
    print(len("Login Area") * "_")

    username = input("Type your username: ")
    password = getpass.getpass("Type your password: ")

    db.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user_data = db.cursor.fetchone()

    if user_data:
        return True, username
    else:
        return False
    
def verify_attempt():
    while True:

        choice = input("Would you like to sign up or sign in? (1 - 2): ")

        if choice not in ["1", "2"]:
            print("Invalid option. Please try again.")
            continue
        
        elif choice == "1":
            is_not_registered = register_user()

            if is_not_registered == True:
                print(f"User registered succesfully")
                
                while True:
                    login_attempt, username = user_login()

                    if login_attempt == True:
                        print(f"\nWelcome {username}")
                        return 1, username
                    else:
                        print("\nInvalid login credentials. Try again.")
                        continue
                    
            else:
                print("\nUsername already exists. Please try again with a different username.")
        
        elif choice == "2":
            while True:
                login_attempt, username = user_login()

                if login_attempt == True:
                    print(f"\nWelcome {username}")
                    return 1, username
                else:
                    print("\nInvalid login credentials. Try again.")
                    continue

def display():
    while True:
        choice = input("What service you would like to use? (1-Tasks, 2-Finances): ")
        if choice not in ["1","2"]:
            print("Invalid Option. Please try again.")
        else:
            break

    return choice

def display_budget():
    while True:
        budget = int(input("Enter your budget: "))
        if budget < 0 or type(budget) != int:
            print("Please enter a valid number greater than zero.")
            continue
        else:
            break
        
    return budget

def display_finances():
    while True:
        choice = input(""" 
1 - Set New Budget
2 - View Expenses
3 - Add Expense
4 - Remove Expense
5 - Edit Expense
6 - Back
 
""")
        
        if choice not in ["1","2","3","4","5","6"]:
            print("Please enter a valid option.")
            continue
        else:
            break

    return choice

def option_3_finances():
    while True:
        expense_name = input("Name of expense: ")
        amount = float(input("Amount spent on this expense: R$"))

        if expense_name == "" or amount == "":
            print("You must fill out all fields.")
            continue
        elif amount < 0 or type(amount) != float:
            print("Please enter a valid positive number.")
            continue
        else:
            break

    return expense_name, amount

def option_4_finances(user_id):
    db = UserDatabase()

    while True:
        expense_name = input("Name of expense: ")
        expense = db.get_expenses_by_name(expense_name=expense_name, user_id=user_id)

        if expense_name == "":
            print("You must fill out the field.")
            continue
        elif expense == None:
            print("This expense does not exist.")
            continue
        else:
            break

    return expense_name

def option_5_finances(user_id):
    db = UserDatabase()
    user_id = db.get_user_id(user_id)

    while True:
        expense_name = input("Type the name of the expense you would like to update: ")
        expense = db.get_expenses_by_name(expense_name=expense_name, user_id=user_id)

        while True:
            print("""What would you like to update:
1 - Expense Name
2 - Expense Value

""")
            choice = input("Enter your choice: ")

            if choice in ["1","2"]:
                break
            elif expense == None:
                print("Expense doesn't exist.")
                continue
            else:
                print("Invalid choice. Please select a valid option.")
                continue

        return expense_name, choice
            

def display_task():
    while True:

        choice = input(""" 
1 - Create Task
2 - Remove Task
3 - Edit Task
4 - See All tasks
5 - Back

""")
        
        if choice not in ["1","2","3","4","5"]:
            print("Please enter a valid option.")
            continue
        else:
            break

    return choice

def option_1_task():

    while True:
        taskname = input("Type the name of the task: ")
        description = input("Describe your task: ")

        if taskname == "" or description == "":
            print("Please fill in all fields.")
            continue
        else:
            break

    return taskname, description

def option_2_task(user_id):
    db = UserDatabase()
    db.get_user_id(user_id)

    while True:
        taskname = input("Type the name of the task you would like to remove: ")
        task = db.get_task_id_by_name(taskname=taskname, user_id=user_id)

        if taskname == "":
            print("Please fill in the task name field.")
            continue

        elif task == None:
            print(f"{taskname} doesn't exist, please provide an existent task")
            continue

        else:
            break
    
    return taskname

def option_3_task(user_id):
    db = UserDatabase()
    user_id = db.get_user_id(user_id)

    while True:
        taskname = input("Type the name of the task you would like to update: ")
        task = db.get_task_id_by_name(taskname=taskname, user_id=user_id)

        while True:
            print("""What would you like to update:
1 - Taskname
2 - Description
3 - Status

""")
            choice = input("Enter your choice: ")

            if choice in ["1","2","3"]:
                break
            elif task == None:
                print(f"{taskname} doesn't exist, please provide an existent task")
                continue
            else:
                print("Invalid choice. Please select a valid option.")

        return taskname, choice