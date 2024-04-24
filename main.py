import sys
import os
from functions import *



def main(current_user: str) -> None:
    """
    The main function of the program, responsible for interacting with the user.

    Parameters:
        current_user (str): The username of currently logged in user.
    """
    while True:
        print(f"{os.linesep}What do you want to do today?")
        print("1. View your to-do list")
        print("2. Create new to-do item")
        print("3. Remove an item")
        print("4. Exit", os.linesep)
        selection = input()
        if selection == '1': show_items(current_user)
        if selection == '2': create_item(current_user)
        if selection == '3': remove_item(current_user)
        if selection == '4': sys.exit(
            os.linesep + 
            "Leaving so soon? Just remember, even Bilbo Baggins had his to-do list: "
            "\n⚬ Adventure awaits, check. "
            "\n⚬ Second breakfast, check. "
            "\n⚬ Keep an eye on that ring, check. "
            "\nUntil we meet again, continue with your tasks like a hobbit on an adventure!")




        

if __name__ == '__main__':
    print("Welcome to Little List-O-Maker Version 1.1")
    currently_logged_user = login_register()
    main(currently_logged_user)