import curses
import multiThreadingExample #Just to be able to use these functions...?

###NOTE: PROBABLY WON'T BE USING CURSES
# IT'S SIMPLY NOT AS VERSATILE AS URWID



def main():
	curses.wrapper(curses_main)
	
	
def curses_main(w):
	#Takes in "window" w
	
	w.addstr("Test!!!\n")
	w.refresh()
	w.addstr("Press any key to exit...")
	w.refresh()
	w.getch()
	
	


main()
