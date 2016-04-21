#-*- coding: UTF-8 -*-
import curses
import curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

while 1:
    c = stdscr.getch()
    if c == ord('p'):
        PrintDocument()
    elif c == ord('q'):
        break  # Exit the while()
    elif c == curses.KEY_HOME:
        x = y = 0
