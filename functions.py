import os
from database import Item, Session, User, User_Item
import bcrypt
import maskpass



def show_items(user_name: str) -> None:
    """
    Display the to-do items of the specified user. If user doesn't have items, will print "No items found for this user".

    Parameters:
        user_name (str): The username of currently logged in user.
    """
    print(os.linesep + "Your to-do list:")
    print("_____")
    with Session() as session:

        query_result = session.query(Item).\
            join(User_Item).\
            join(User).\
            filter(User.username == user_name).\
            all()

        if not query_result:
            print(os.linesep + "No items found for this user.")
        else:
            for item in query_result:
                item_id = item.item_id
                item_name = item.name
                item_description = item.description
                item_time = item.time.strftime("%d-%m-%Y %H:%M")

                print(f"ID number {item_id}: {item_name}")
                print(f"Time added: {item_time}")
                print("Description:")
                print(os.linesep + f"{item_description}")
                print("_____" + os.linesep)
    return None



def create_item(user_name: str) -> None:
    """
    Creates a new item for the currently logged in user. Asks for item name and description, by default adds current time as the time created.
    Commits the changes to the database.

    Parameters:
        user_name (str): The username of currently logged in user.
    """
    print("Name for the item:")
    item_name = input()
    print("Description for the item:")
    item_description = input()    

    with Session() as session:
        new_item = Item(name = item_name, description = item_description)
        session.add(new_item)

        user = session.query(User).filter(User.username == user_name).first()
        new_user_item = User_Item(item_id = new_item.item_id, user_id = user.user_id)
        session.add(new_user_item)
        session.commit()
    return None



def remove_item(user_name: str) -> None:
    """
    Removes an item based on ID number and currently logged in user.
    If user doesn't have items prints "You should add some items first".
    If user tries to remove an item that is not assocciated with the logged in user, prints "Invalid ID".

    Parameters:
        user_name (str): The username of currently logged in user.
    """
    with Session() as session:
        item_amount = session.query(Item).\
            join(User_Item).\
            join(User).\
            filter(User.username == user_name).\
            count()
        if item_amount < 1:
            print(os.linesep + "You should add some items first.")
            return
        try:
            print(os.linesep +"Give the ID to remove:")
            item_id = int(input())

            removable_item  = session.query(Item).\
                join(User_Item).\
                join(User).\
                filter(User.username == user_name, Item.item_id == item_id).\
                first()
            if removable_item is None:
                print(os.linesep + "Invalid ID!")
            else:
                session.delete(removable_item)
                session.commit()
                print(os.linesep + f"Deleted item '{removable_item.name}'")                
        except ValueError:
            print(os.linesep + "Invalid ID")
    return None



def hash_password_bcrypt(password: str, salt: bytes) -> bytes:
    """
    Hashes the provided password using bcrypt.

    Parameters:
        password (str): The password to be hashed.
        salt (bytes): The salt to be used for hashing.

    Returns:
        hashed_password (bytes): The hashed password.
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password



def verify_password_bcrypt(password: str, hashed_password: bytes) -> bool:
    """
    Verifies if the provided password matches the hashed password using bcrypt.

    Parameters:
        password (str): The password provided by the user.
        hashed_password (bytes): The hashed password stored in the database.

    Returns:
        bool: True if the provided password matches the hashed password, False if not.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)



def login(provided_password: str, username: str) -> None:
    """
    Validate the provided username and password for login.

    If the username and password match an existing user, prints a welcome message.
    If the username and password do not match any existing user, prints an error message.


    Parameters:
        provided_password (str): The password provided by the user.
        username (str): The username provided by the user.
    """
    with Session() as session:
        hashed_password = session.query(User.password).filter(User.username == username).first()
        verify_hashed_password = verify_password_bcrypt(provided_password, hashed_password[0])
        if not verify_hashed_password:
            print(os.linesep +"Invalid password or username!" + os.linesep)
            login_register()
        else:
            print(os.linesep + f"Welcome {username}!")          
    return None



def login_register() -> str:
    """
    Asks the user to login or register. If user wants to login, login function is called. If user tries to login and there
    are no users in the database, prints an error message to register first. 

    Returns:
        str: The username of the logged-in user or the newly registered user.
    """
    with Session() as session:
        while True:
            try:
                user_input = input("Do you want to login or register? ")
                if user_input.lower() == "login":
                    login_username = input("Username: ")
                    login_password = maskpass.askpass()
                    login(login_password, login_username)
                    return login_username

                elif user_input.lower() == "register":
                    new_username = input("Write new username: ")
                    new_password = maskpass.askpass()
                    check_if_exists = session.query(User).filter(User.username == new_username).first()
                    if check_if_exists is None:
                        new_salt = bcrypt.gensalt(rounds = 4)
                        new_hashed_password = hash_password_bcrypt(new_password, new_salt)
                        new_user = User(username = new_username, password = new_hashed_password)
                        session.add(new_user)
                        session.commit()
                        print(os.linesep + f"New user {new_username} created successfully.")
                        return new_username

                    else:
                        print(os.linesep + "Username is taken, try again!" + os.linesep)
                    
                else:
                    print(os.linesep + "Write either 'register' or 'login'." + os.linesep)
            except TypeError:
                print(os.linesep + "You need to register first!" + os.linesep)
