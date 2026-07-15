import os
import sys
import msvcrt
import json
import time
from .Paths import AppDir


def clear():
    os.system("cls")


USERS_FILE = os.path.join(AppDir, "Settings", "users.json")


# =====================================
# PASSWORD INPUT
# =====================================

def input_password(prompt="Password: "):
    print(prompt, end="", flush=True)

    password = ""

    while True:

        char = msvcrt.getch()

        # ENTER
        if char in {b"\r", b"\n"}:
            print()
            break

        # BACKSPACE
        elif char == b"\x08":

            if len(password) > 0:
                password = password[:-1]

                sys.stdout.write("\b \b")
                sys.stdout.flush()

        # NORMAL CHARACTERS
        elif len(char) == 1 and char.isascii():

            try:
                decoded = char.decode("utf-8")

                password += decoded

                print("*", end="", flush=True)

            except:
                pass

    return password


# =====================================
# USERS
# =====================================

def load_users():

    try:

        with open(USERS_FILE, "r") as file:
            return json.load(file)

    except FileNotFoundError:

        return {}

    except json.JSONDecodeError:

        print("users.json is corrupted.")
        time.sleep(2)

        return {}


# =====================================
# LOCKSCREEN
# =====================================

def lockscreen():

    while True:

        users = load_users()

        # SEM USUÁRIOS = AUTOLOGIN
        if not users:

            time.sleep(1)

            return "Guest"

        clear()

        print("===================================")
        print("         TMDOS LOCKSCREEN")
        print("===================================\n")

        username = input("Username: ").strip()

        password = input_password("Password: ").strip()

        if username in users:

            if users[username] == password:

                print(f"\nWelcome back, {username}!")

                input("\nPress Enter to continue...")

                return username

            else:

                print("\nAccess denied.")
                time.sleep(1)

        else:

            print("\nUnknown user.")
            time.sleep(1)