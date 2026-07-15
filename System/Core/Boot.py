import os
import sys
import time
import platform
import subprocess
from datetime import datetime

try:
    import psutil
except Exception:
    psutil = None

# =====================================
# INIT VARS
# =====================================

Boot_delay = 0.3

kernel_name = "TMKernel"
kernel_version = "v1.0"

shell_name = "TMDOS"
shell_version = "0.7"
shell_build = "17"
development_process = "Beta 1"

# =====================================
# UTIL
# =====================================

def get_gpu():

    try:

        gpu = subprocess.check_output(
            "wmic path win32_VideoController get name",
            shell=True
        ).decode(errors="ignore").split("\n")[1].strip()

        return gpu if gpu else "Unknown GPU"

    except Exception:
        return "Unknown GPU"


def clear():

    os.system("cls" if os.name == "nt" else "clear")


def pause():

    os.system("pause" if os.name == "nt" else "read -p 'Press Enter to continue...'")

# =====================================
# SYSINFO SAFE
# =====================================

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

# =====================================
# BOOT
# =====================================

def boot_screen():

    os.system("title TMDOS")
    
    clear()

    print("====================================")
    print(f"{shell_name} {shell_version}")
    print("====================================")

    print("\nInitializing system...\n")

    steps = [
        "Loading kernel",
        "Checking users database",
        "Starting input system",
        "Preparing shell environment",
        "Loading virtual filesystem",
        "Initializing command shell"
    ]

    for step in steps:

        print(f"[BOOT] {step}...")

        time.sleep(Boot_delay)

    kernel_info = [
        f"Kernel name: {kernel_name}",
        f"Kernel version: {kernel_version}",
    ]

    for info in kernel_info:

        print(f"[KERNEL] {info}")

        time.sleep(Boot_delay)

    equipment = [
        f"CPU: {platform.processor()}",
        f"CPU architecture: {platform.machine()}",
        f"RAM: {get_ram()}",
        f"GPU: {get_gpu()}"
    ]

    for item in equipment:

        print(f"[COMPONENT] {item}")

        time.sleep(Boot_delay)

    current_datetime = [
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        f"Time: {datetime.now().strftime('%H:%M:%S')}"
    ]

    for dt in current_datetime:

        print(f"[TIME] {dt}")

        time.sleep(Boot_delay)

    print("\nBoot sequence:\n")

    bar_length = 30

    for i in range(bar_length + 1):

        bar = "█" * i + "░" * (bar_length - i)

        percent = int((i / bar_length) * 100)

        sys.stdout.write(f"\r[{bar}] {percent}%")

        sys.stdout.flush()

        time.sleep(Boot_delay / 6)

    print("\nBoot completed successfully.\n")

    time.sleep(1)

    print("\nStarting TMDOS...\n")

    time.sleep(1)

# =====================================
# START
# =====================================

if __name__ == "__main__":

    boot_screen()