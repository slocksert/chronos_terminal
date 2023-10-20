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
    password = input("Type your password: ")

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
    password = input("Type your password: ")

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
    choice = input(""" 
1 - Create Task
2 - Remove Task
3 - Edit Task
4 - See all tasks
5 - Quit

""")
    return choice

def option_1_data():
    while True:
        taskname = input("Type the name of the task: ")
        description = input("Describe your task: ")

        if taskname == "" or description == "":
            print("Please fill in all fields.")
            continue
        else:
            break

    return taskname, description

def option_2_data():
    while True:
        taskname = input("Type the name of the task you would like to remove: ")

        if taskname == "":
            print("Please fill in the task name field.")
            continue
        else:
            break
    
    return taskname

def option_3_data():
    while True:
        taskname = input("Type the name of the task you would like to update: ")

        while True:
            print("""What would you like to update:
1 - Taskname
2 - Description
3 - Status

""")
            choice = input("Enter your choice: ")

            if choice in ["1", "2", "3"]:
                break
            else:
                print("Invalid choice. Please select a valid option.")

        return taskname, choice