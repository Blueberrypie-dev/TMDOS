import subprocess
from pathlib import Path
import sys
import shutil
import time
import os
import platform
from datetime import datetime
import webbrowser
import psutil
# =====================================
# UTIL
# =====================================

shell_name = "TMDOS Command Prompt"

shell_version = "0.0.8"

shell_build = "18"



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

def get_gpu():

    try:

        gpu = subprocess.check_output(
            "wmic path win32_VideoController get name",
            shell=True
        ).decode(errors="ignore").split("\n")[1].strip()

        return gpu if gpu else "Unknown GPU"

    except Exception:
        return "Unknown GPU"

def quit_shell():

    clear()

    print("Shutting down TMOS...")

    time.sleep(1)

    sys.exit()

def show_sysinfo():

    print("\n=== SYSTEM INFO ===")

    print("OS:", shell_name + " " + shell_version + " Build " + shell_build)

    print("CPU:", platform.processor())

    print("RAM:", get_ram())

    print("CPU:", platform.processor())

    print("GPU:", get_gpu())

def get_ram():

    try:

        # Usa psutil se disponível
        if psutil is not None:

            ram = psutil.virtual_memory().total / (1024 ** 3)

            return f"{round(ram, 2)} GB"

        # Fallback Windows
        if platform.system() == "Windows":

            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):

                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()

            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)

            ctypes.windll.kernel32.GlobalMemoryStatusEx(
                ctypes.byref(stat)
            )

            ram = stat.ullTotalPhys / (1024 ** 3)

            return f"{round(ram, 2)} GB"

        # Fallback Linux/macOS
        else:

            pages = os.sysconf("SC_PHYS_PAGES")
            page_size = os.sysconf("SC_PAGE_SIZE")

            ram = pages * page_size / (1024 ** 3)

            return f"{round(ram, 2)} GB"

    except Exception:

        return "Unknown"

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
TSKS        - Show processes
KILLTSK     - Kill process
SDWN        - Shutdown PC
REBOOT      - Reboot PC
EXIT        - Exit TMOS
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
