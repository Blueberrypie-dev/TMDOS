import os
from System.Core.Paths import UsersFile
import json

def clear():
    os.system("cls")


def create_account():
    clear()
    print("=== Create New Account ===")
    name = input("Enter the new username: ")
    password = input("Enter the new user's password: ")

    name = name.strip()

    

    try:
        with open(UsersFile, "r") as f:
            users = json.load(f)
    except:
        users = {}

    if not name:
        print("❌ Invalid username.")
        input("Press ENTER to continue...")
        clear()
        return
    
    else:
        # Salva
        if name in users:
            print("❌ User already exists.")
            input("Press ENTER to continue...")
            clear()
            return
        else:
            # Adiciona novo usuário
            users[name] = password
            with open(UsersFile, "w") as f:
                json.dump(users, f, indent=4)

        print("User created successfully!")
        input("Press ENTER to continue...")
        clear()