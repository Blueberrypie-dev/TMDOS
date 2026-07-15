from System.Core.Boot import clear
from System.Core.Paths import AppDir
import json

UsersFile = AppDir / "Settings" / "users.json"


def delete_account():

    usuario = input("Username to delete: ")

    try:

        with open(UsersFile, "r", encoding="utf-8") as f:
            users = json.load(f)

        if usuario not in users:
            print("❌ User not found.")
            return

        del users[usuario]

        with open(UsersFile, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)

        print("✅ User deleted successfully.")

    except FileNotFoundError:
        print("❌ users.json not found.")

    except json.JSONDecodeError:
        print("❌ Invalid JSON.")
    clear()