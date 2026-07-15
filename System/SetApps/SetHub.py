import os
import curses
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from System.SetApps.LogHub import login_settings
    
menu = [
    "Login Settings",
    "Exit"
]

def clear():
    os.system("cls")

# =========================================
# DRAW BOX
# =========================================

def draw_box(stdscr, y, x, h, w, color):

    # Evita desenhar fora da tela
    max_y, max_x = stdscr.getmaxyx()
    if y + h >= max_y or x + w >= max_x:
        return

    # Cantos
    stdscr.addch(y, x, "┌", color)
    stdscr.addch(y, x + w, "┐", color)
    stdscr.addch(y + h, x, "└", color)
    stdscr.addch(y + h, x + w, "┘", color)

    # Horizontais
    for i in range(1, w):
        stdscr.addch(y, x + i, "─", color)
        stdscr.addch(y + h, x + i, "─", color)

    # Verticais
    for i in range(1, h):
        stdscr.addch(y + i, x, "│", color)
        stdscr.addch(y + i, x + w, "│", color)


# =========================================
# ACTIONS
# =========================================

def logset(stdscr):

    curses.def_prog_mode()   # salva estado atual
    curses.endwin()          # pausa o curses

    curses.wrapper(login_settings)

    input("Pressione ENTER para voltar...")

    curses.reset_prog_mode() # restaura o curses
    stdscr.refresh()



# =========================================
# MAIN LOOP
# =========================================

def settings(stdscr):

    curses.curs_set(0)
    curses.start_color()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)   # fundo azul
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # selecionado

    BLUE = curses.color_pair(1)
    SELECT = curses.color_pair(2)

    current = 0

    while True:

        stdscr.clear()
        h, w = stdscr.getmaxyx()

        stdscr.bkgd(" ", BLUE)

        # =========================================
        # TITLE BOX
        # =========================================

        title_w = 46
        title_x = w // 2 - title_w // 2

        draw_box(stdscr, 3, title_x, 2, title_w, BLUE)

        title = "TMOS SETTINGS HUB"

        stdscr.addstr(
            4,
            w // 2 - len(title) // 2,
            title,
            BLUE | curses.A_BOLD
        )

        # =========================================
        # MENU BOX
        # =========================================

        box_w = 46
        box_h = 14
        box_x = w // 2 - box_w // 2
        box_y = 8

        draw_box(stdscr, box_y, box_x, box_h, box_w, BLUE)

        for i, item in enumerate(menu):

            item_y = box_y + 2 + i * 2
            item_x = box_x + 3

            if i == current:
                stdscr.addstr(
                    item_y,
                    item_x,
                    f"> {item}".ljust(40),
                    SELECT
                )
            else:
                stdscr.addstr(
                    item_y,
                    item_x,
                    f"  {item}",
                    BLUE
                )

        # =========================================
        # FOOTER
        # =========================================

        footer_y = h - 4
        draw_box(stdscr, footer_y, 2, 2, w - 6, BLUE)

        footer = "UP/DOWN = Navigate     ENTER = Select     ESC = Exit"

        stdscr.addstr(
            footer_y + 1,
            w // 2 - len(footer) // 2,
            footer,
            BLUE | curses.A_BOLD
        )

        stdscr.refresh()

        # =========================================
        # INPUT
        # =========================================

        key = stdscr.getch()

        # Navegação
        if key == curses.KEY_UP:
            current = (current - 1) % len(menu)

        elif key == curses.KEY_DOWN:
            current = (current + 1) % len(menu)

        # ENTER
        elif key in [10, 13]:

            selected = menu[current]

            if selected == "Exit":
                break

            elif selected == "Login Settings":
                login_settings(stdscr)

        # ESC
        elif key == 27:
            break