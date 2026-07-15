import curses
import os

def bsod(stdscr):
    os.system("Title TMDOS - Error")
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    stdscr.bkgd(curses.color_pair(1))
    screentotal = stdscr.getmaxyx()
    textplace = screentotal[0] // 2
    text = "      Ooops! Looks like something went wrong. Please restart the system."
    text += "\n                If the problem persists, please reinstall TMDOS."
    stdscr.addstr(10, 5, text)
    stdscr.getch()
    stdscr.refresh()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()