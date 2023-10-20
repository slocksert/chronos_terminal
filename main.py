from models import User
from utils import verify_attempt, display, option_1_data, option_2_data, option_3_data


def main():
    print("\nInitializing Chronos App\n")
    attempt, username = verify_attempt()

    if attempt == 1:
        user = User(username)
        
        user_id = user.get_user_id(username)
        user.user_id = user_id

        while True:
            choice = display()

            if choice not in ["1","2","3","4","5"]:
                print("Invalid input. Please enter a valid option.")
                continue
            
            elif choice == "1":
                taskname, description = option_1_data()
                user.create_task(taskname=taskname, description=description)
                print(f"'{taskname}' created")

            elif choice == "2":
                taskname = option_2_data()   
                user.delete_task(taskname)
                print(f"'{taskname}' removed")

            elif choice == "3":
                taskname, choice = option_3_data()
                user.update_task_db(taskname=taskname, choice=choice, user_id=user_id)

            elif choice == "4":
                for tasks in user.get_tasks():
                    print(f"Taskname: {tasks[2]}, Description: {tasks[3]}, Status: {tasks[4]}")
            
            elif choice == "5":
                quit("Closing Chronos app")
                

if __name__ == "__main__":
    main()