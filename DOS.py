import subprocess
from pathlib import Path
import sys
import shutil
import time
import os
import platform
import curses
from datetime import datetime
import webbrowser
from System.Core.Paths import AppDir
from System.Core.BSOD import bsod
# =====================================
# UTIL
# =====================================

required_files = [
    AppDir / "System" / "Core" / "Login.py",
    AppDir / "System" / "Core" / "Paths.py",
    AppDir / "System" / "SetApps" / "LogHub.py",
    AppDir / "System" / "Core" / "Boot.py",
    AppDir / "System" / "SetApps" / "SetHub.py",
    AppDir / "System" / "SetApps" / "Countcreate.py",
    AppDir / "System" / "SetApps" / "Countedit.py"
]

missing = [file for file in required_files if not file.exists()]

if missing:

    os.system("type nul > " + str(AppDir / "System" / "Core" / "Logs" / "boot_error.log"))
    
    with open(AppDir / "System" / "Core" / "Logs" / "boot_error.log", "w", encoding="utf-8") as log:

        log.write("Missing files:\n\n")

        for file in missing:
            log.write(str(file) + "\n")

    curses.wrapper(bsod)

    sys.exit()
else:    
    from System.SetApps.SetHub import settings
    from System.Core.Boot import boot_screen, get_gpu, get_ram, kernel_name, kernel_version, shell_build, shell_name, shell_version
    from System.Core.Login import lockscreen
 
  
boot_screen()

users_file = os.path.join(AppDir, "settings", "users.json")

username = lockscreen()

current_dir = Path("C:\\")

root_dir = os.path.splitdrive(current_dir)[0] + "\\"

def clear():
    os.system("cls")

def pause():
    os.system("pause")

# =====================================
# COMMANDS
# =====================================

variaveis = {}

def whoami():
    print(username)

def quit_shell():

    clear()

    print("Shutting down TMOS...")

    time.sleep(1)

    sys.exit()

def show_sysinfo():

    print("\n=== SYSTEM INFO ===")

    print("OS:", shell_name + " " + shell_version + " Build " + shell_build)

    print("Kernel:", kernel_name + " " + kernel_version)

    print("CPU:", platform.processor())

    print("RAM:", get_ram())

    print("CPU:", platform.processor())

    print("GPU:", get_gpu())

    print("Kernel Version:", kernel_name + " " + kernel_version)

def run_program(cmd):

    global current_dir

    parts = cmd.split(" ", 1)

    if len(parts) < 2:
        print("Usage: RUN <file_or_url>")
        return

    target = parts[1].strip().strip('"')

    # 🌐 DETECTA LINK
    if target.startswith("http://") or target.startswith("https://"):

        print("Opening web page...")
        webbrowser.open(target)
        return

    # 📁 SENÃO: TRATA COMO ARQUIVO LOCAL
    if not os.path.isabs(target):
        target = os.path.join(current_dir, target)

    if os.path.exists(target):

        try:
            os.startfile(target)
            print("Program started.")
        except Exception as e:
            print(f"Error: {e}")

    else:
        print("File not found.")

def create_file(cmd):

    parts = cmd.split(" ", 1)

    if len(parts) < 2:
        print("Usage: NEW <file>")
        return

    filename = parts[1].strip().strip('"')

    filepath = os.path.join(current_dir, filename)

    try:
        with open(filepath, "w") as f:
            pass

        print("File created:", filename)

    except Exception as e:
        print(f"Error: {e}")

def remove_file(cmd):

    parts = cmd.split(" ", 1)

    if len(parts) < 2:
        print("Usage: REF <file_or_folder>")
        return

    target = parts[1].strip().strip('"')

    path = os.path.join(current_dir, target)

    if not os.path.exists(path):
        print("Not found.")
        return

    try:
        # 📁 PASTA
        if os.path.isdir(path):
            shutil.rmtree(path)
            print("Folder removed.")

        # 📄 ARQUIVO
        else:
            os.remove(path)
            print("File removed.")

    except PermissionError:
        print("Permission denied.")

    except Exception as e:
        print(f"Error: {e}")

def edit_file(filename):

    filepath = os.path.join(current_dir, filename)

    try:

        os.system(f'notepad "{filepath}"')

    except Exception as e:

        print(f"Error: {e}")

def list_directory():

    try:

        files = os.listdir(current_dir)

        if len(files) == 0:

            print("Directory is empty.")

        else:

            for item in files:

                print(item)

    except Exception as e:

        print(f"Error: {e}")

def change_directory(target):

    global current_dir

    target = target.strip('"')

    new_dir = (
        target
        if os.path.isabs(target)
        else os.path.join(current_dir, target)
    )

    if os.path.isdir(new_dir):

        current_dir = new_dir

    else:

        print("Directory not found.")

def DISP(args):

    """
    Comando equivalente ao ECHO do CMD
    """

    # Se não houver texto
    if not args:
        print()
        return

    # =====================================
    # TRANSFORMA EM TEXTO CORRETAMENTE
    # =====================================

    if isinstance(args, list):
        texto = " ".join(args)
    else:
        texto = str(args)

    # =====================================
    # SUBSTITUIR VARIÁVEIS
    # =====================================

    for nome, valor in variaveis.items():

        texto = texto.replace(f"%{nome}%", str(valor))
        texto = texto.replace(f"%{nome.lower()}%", str(valor))

    # =====================================
    # PRINT
    # =====================================

    print(texto)

def SET(args):

    # =====================================
    # TRANSFORMA EM TEXTO
    # =====================================

    if isinstance(args, list):
        comando = " ".join(args)
    else:
        comando = str(args)

    comando = comando.strip()

    # =====================================
    # MOSTRAR TODAS
    # =====================================

    if comando == "":

        for nome, valor in variaveis.items():
            print(f"{nome}={valor}")

        return

    # =====================================
    # CRIAR VARIÁVEL
    # =====================================

    if "=" in comando:

        nome, valor = comando.split("=", 1)

        nome = nome.strip().upper()
        valor = valor.strip()

        variaveis[nome] = valor

        return

    # =====================================
    # MOSTRAR VARIÁVEL
    # =====================================

    nome = comando.upper()

    if nome in variaveis:
        print(f"{nome}={variaveis[nome]}")
    else:
        print("Variável não encontrada.")

    # =====================================
    # CRIAR VARIÁVEL
    # =====================================

    if "=" in comando:

        nome, valor = comando.split("=", 1)

        nome = nome.strip().upper()
        valor = valor.strip()

        variaveis[nome] = valor

        return

    # =====================================
    # MOSTRAR VARIÁVEL
    # =====================================

    nome = comando.strip().upper()

    if nome in variaveis:

        print(f"{nome}={variaveis[nome]}")

    else:

        print("Variável não encontrada.")

# =====================================
# SHELL HEADER
# =====================================

clear()

print("===============================================")
print(f"            {shell_name} v{shell_version} Build {shell_build}")
print("===============================================")

# =====================================
# MAIN LOOP
# =====================================

while True:

    try:

        cmd = input(f"\n[{current_dir}]> ").strip()

        if len(cmd) == 0:

            continue

        parts = cmd.split(" ", 1)

        command = parts[0].upper()

        args = []

        if len(parts) > 1:
            args = parts[1]


        # =====================================
        # EXIT
        # =====================================

        if command == "EXIT":

            quit_shell()     

        # =====================================
        # LOCK
        # =====================================

        elif command == "LOCK":

            lockscreen()

            clear()
        
        # =====================================
        # DISP
        # =====================================

        elif command == "DISP":

            DISP(args)
            
        # =====================================
        # TIME
        # =====================================

        elif command == "TIME":

            print(datetime.now().strftime("%H:%M:%S"))

        # =====================================
        # REF
        # =====================================
        elif command == "REF":
            remove_file(cmd)
            
        # =====================================
        # WHOAMI
        # =====================================

        elif command == "WHOAMI":

            whoami()

        # =====================================
        # DATE
        # =====================================

        elif command == "DATE":

            print(datetime.now().strftime("%d/%m/%Y"))
        
        # =====================================
        # SET
        # =====================================
        elif command == "SET":
            SET(args)

        # =====================================
        # VER
        # =====================================

        elif command == "VER":

            print(f"{shell_name} v{shell_version} Build {shell_build}")

        # =====================================
        # SYSINFO
        # =====================================

        elif command == "SYSINFO":

            show_sysinfo()

        # =====================================
        # CLEAN
        # =====================================

        elif command == "CLEAN":

            clear()

        # =====================================
        # ROOT
        # =====================================

        elif command == "ROOT":

            current_dir = root_dir
        # =====================================
        # SDWN
        # =====================================

        elif command == "SDWN":

                os.system("shutdown /s /t 0")
        
        # =====================================
        # REBOOT
        # =====================================

        elif command == "REBOOT":

                os.system("shutdown /r /t 0")

        # =====================================
        # BACK
        # =====================================

        elif command == "BACK":

            parent = os.path.dirname(current_dir)

            if parent:

                current_dir = parent
        
        # =====================================
        # SETTINGS
        # =====================================
        elif command == "SETTINGS":

            curses.wrapper(settings)
        # =====================================
        # GO
        # =====================================

        elif command == "GO":

            if len(args) == 0:

                print("Usage: GO <folder>")

                continue

            change_directory(args)

        # =====================================
        # VD
        # =====================================

        elif command == "VD":

            list_directory()

        # =====================================
        # NEW
        # =====================================

        elif command == "NEW":
            create_file(cmd)

        # =====================================
        # EDIT
        # =====================================

        elif command == "EDIT":

            if len(args) == 0:

                edit_file(input("Enter file name to edit: "))

                continue

            edit_file(args)

        # =====================================
        # RUN
        # =====================================

        elif command == "RUN":

            run_program(cmd)

        # =====================================
        # TSKS
        # =====================================

        elif command == "TSKS":

            try:

                result = subprocess.run(
                    ["tasklist"],
                    capture_output=True,
                    text=True
                )

                print(result.stdout)

            except Exception as e:

                print(f"Error: {e}")

        # =====================================
        # KILLTSK
        # =====================================

        elif command == "KILLTSK":

            if len(args) == 0:

                print("Usage: KILLTSK <process_name>")

                continue

            proc_name = args.strip()

            try:

                subprocess.run(
                    ["taskkill", "/F", "/IM", proc_name],
                    check=True
                )

                print(f"Process '{proc_name}' terminated.")

            except subprocess.CalledProcessError:

                print(f"Failed to terminate '{proc_name}'.")

        # =====================================
        # HELP
        # =====================================

        elif command == "HELP":

            print("""
Available Commands:

TIME        - Show current time
DATE        - Show current date
VER         - Show TMOS version
SYSINFO     - Show system information
CLEAN       - Clear screen
ROOT        - Go to drive root
BACK        - Go to parent directory
GO          - Change directory
VD          - View directory contents
NEW         - Create file
EDIT        - Edit file
RUN         - Run program/file
LOCK        - Lock system
TSKS        - Show processes
KILLTSK     - Kill process
SDWN        - Shutdown PC
REBOOT      - Reboot PC
EXIT        - Exit TMOS
SETTINGS    - Open settings hub
""")

        # =====================================
        # UNKNOWN
        # =====================================

        else:

            print("Bad command or file name.")

    except KeyboardInterrupt:

        print("\nUse EXIT to close TMOS.")

    except Exception as e:

        print(f"System Error: {e}")
