from database import UserDatabase
from utils import verify_attempt, display, option_1_task, option_2_task, option_3_task, display_finances, display_task, display_budget, option_3_finances, option_4_finances, option_5_finances


def main():
    print("\nInitializing Chronos App\n")
    attempt, username = verify_attempt()

    if attempt == 1:
        user = UserDatabase()
        user_id = user.get_user_id(username)

        def display_all_tasks(user_id):
            for tasks in user.get_tasks(user_id=user_id):
                print(f"Taskname: {tasks[2]}, Description: {tasks[3]}, Status: {tasks[4]}")

        def display_all_finances(user_id):
            for finances in user.get_finances(user_id=user_id):
                print(f"Item: {finances[2]}, Value: R${finances[3]}")

        while True:
            choice = display()

            if choice == "1":
                while True:
                    choice = display_task()

                    if choice == "1":
                        taskname, description = option_1_task()
                        user.create_task(taskname=taskname, description=description, user_id=user_id)
                        print(f"'{taskname}' created")

                    elif choice == "2":
                        display_all_tasks(user_id=user_id)
                        taskname = option_2_task()   
                        user.delete_task(taskname=taskname, user_id=user_id)
                        print(f"'{taskname}' removed")

                    elif choice == "3":
                        display_all_tasks(user_id=user_id)
                        taskname, choice = option_3_task(user_id=user_id)
                        user.update_task(taskname=taskname, choice=choice, user_id=user_id)

                    elif choice == "4":
                        display_all_tasks(user_id=user_id)
                    
                    elif choice == "5":
                        break
            
            else:
                while True:
                    finances = user.get_budget(user_id=user_id)

                    if finances == 0:
                        budget = display_budget()
                        user.set_budget(budget=budget, user_id=user_id)
                        print(f"New budget: R${budget}")
                        continue
                    else:
                        total_expenses = user.get_total_expenses(user_id=user_id)
                        if total_expenses == 0:
                            print(f"\nActual Budget: R${finances}")
                            print(f"Total used: R${total_expenses} of R${finances}")
                        else:
                            total_expenses = sum(total_expenses)
                            print(f"\nActual Budget: R${finances}")
                            print(f"Total used: R${total_expenses} of R${finances}")
                        
                        if total_expenses > finances:
                            print(f"You went over the budget, remove expenses or set a new budget.")
                        elif total_expenses == finances:
                            print(f"Your expense spend is equal to your budget.")

                        choice = display_finances()
                        
                        if choice == "1":
                            new_budget = display_budget()
                            user.set_budget(user_id=user_id, budget=new_budget)
                            print(f"New budget: R${new_budget}")
                        
                        elif choice == "2":
                            display_all_finances(user_id=user_id)

                        elif choice == "3":
                            expense_name, expense_value = option_3_finances()
                            user.add_expense(expense_name=expense_name ,expense_value=expense_value, user_id=user_id)
                            print(f"{expense_name} added, Value: R${expense_value}")

                        elif choice == "4":
                            expense_name = option_4_finances(user_id=user_id)
                            user.remove_expense(expense_name=expense_name, user_id=user_id)

                        elif choice == "5":
                            expense_name, choice = option_5_finances(user_id=user_id)
                            user.update_expense(choice=choice, expense_name=expense_name, user_id=user_id)

                        elif choice == "6":
                            break

if __name__ == "__main__":
    main()