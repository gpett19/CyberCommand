import urwid

#Creates the basic class for a menu button
# Takes in the button text (caption), and callback(action to be taken)
#This should be fine.
class MenuButton(urwid.Button):
	def __init__(self, caption, callback):
		super(MenuButton, self).__init__("")
		#Connects the click signal to execute whatever the callback is
		urwid.connect_signal(self, 'click', callback)
		#Just stylizes the text...
		self._w = urwid.AttrMap(urwid.SelectableIcon(['  \N{BULLET} ', caption], 2), None, 'selected')

#Actually creates a menu frame...
# Takes in the caption (menu title), and a list of choices
# to be made into buttons
class Menu(urwid.WidgetWrap):
	def __init__(self, caption, choices):
		super(Menu, self).__init__(MenuButton([caption, "\N{HORIZONTAL ELLIPSIS}"], self.open_menu))
		line = urwid.Divider('\N{LOWER ONE QUARTER BLOCK}')
		#Creates the "list" of choices
		listbox = urwid.ListBox(urwid.SimpleFocusListWalker([
			urwid.AttrMap(urwid.Text(["\n", caption]), 'heading',),
			urwid.AttrMap(line, 'line'),
			urwid.Divider()] + choices + [urwid.Divider()]))
		self.menu = urwid.AttrMap(listbox, 'options')
	def open_menu(self, button):
		top.open_box(self.menu)

def exit_menu(key):
	raise urwid.ExitMainLoop()

#Creates an "Info Button" that is designed to basically do nothing on click.
#Basically just stores info.
class InfoButton(urwid.Button):
	def __init__(self, caption):
		super(InfoButton, self).__init__("")
		self._w = urwid.AttrMap(urwid.SelectableIcon(['  \N{BULLET} ', caption], 2), None, 'selected')
		
		
#Defines a "Bot Choice" class that will contain all the information
# for bots
# "info" will be a list of strings giving bot info
# Assumes i is properly formatted
class InfoButtonList(urwid.Pile):
	def __init__(self, botInfo):
		lst = []
		for b in botInfo:
			lst.append(InfoButton(b))
		super(InfoButtonList, self).__init__(lst)
		#super(BotChoice, self).__init__(InfoButton(botInfo))

class CommandMenu(urwid.WidgetWrap):
	def __init__(self, caption):
		super(CommandMenu, self).__init__(MenuButton([caption, "\N{HORIZONTAL ELLIPSIS}"], self.open_menu))
		line = urwid.Divider('\N{LOWER ONE QUARTER BLOCK}')




#Random Junk that just gives colors & junk
# You can safely ignore this unless you care a lot
# about colors for some reason
palette = [
    (None,  'light gray', 'black'),
    ('heading', 'black', 'light gray'),
    ('line', 'black', 'light gray'),
    ('options', 'dark gray', 'black'),
    ('focus heading', 'white', 'dark red'),
    ('focus line', 'black', 'dark red'),
    ('focus options', 'black', 'light gray'),
    ('selected', 'white', 'dark blue')]
focus_map = {
    'heading': 'focus heading',
    'options': 'focus options',
    'line': 'focus line'}


#Class that deals with all the horizontal menu construction and junk.
# We can rearrange this to have like other menus or stuff instead
# But let's go for this for now.
class HorizMenus(urwid.Columns):
	def __init__(self):
		super(HorizMenus, self).__init__([], dividechars = 1)
	
	def open_box(self, box):
		if self.contents:
			del self.contents[self.focus_position + 1:]
		self.contents.append((urwid.AttrMap(box, 'options', focus_map),
				self.options('given', 24)))
		self.focus_position = len(self.contents) - 1
		
	#No clue if this will work
	# Basically takes the "top" variable from the other class and sets it as a global
	# here
	#Stupid as fuck, and 1000% terrible code, but let's see if it works...
	def make_self(self, topIn):
		global top
		top = topIn
		
