#Creates the basic class for a menu button
# Takes in the button text (caption), and callback(action to be taken)
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

#Defines a "Bot Choice" class that will contain all the information
# for bots
# "info" will be a list of strings giving bot info
class BotChoice(urwid.WidgetWrap):
	def __init__(self, botNum, info):
		super(BotChoice, self).__init__(MenuButton(botNum, self.item_chosen))
		self.botNum = botNum
	def item_chosen(self, button):
		infoList = []
		infoList.append(urwid.Text(["Viewing information for ", self.caption, "\n"]))
		for i in info:
			infoList.append(urwid.Text([i], ))
			

#Random Junk that just gives colors & junk
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


class HorizMenus(urwid.Columns):
	def __init__(self):
		super(HorizMenus, self).__init__([], dividechars = 1)
	
	def open_box(self, box):
		if self.contents:
			del self.contents[self.focus_position + 1:]
		self.contents.append((urwid.AttrMap(box, 'options', focus_map),
				self.options('given', 24)))
		self.focus_position = len(self.contents) - 1
