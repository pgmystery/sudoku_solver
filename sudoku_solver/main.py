# -*- coding: utf-8 -*-
import os
import sys
try:
	from thread import start_new_thread  # Python 2
except ImportError:
	from _thread import start_new_thread  # Python 3

from kivy.app import App
from kivy.uix.widget import Widget

from interface import Interface
from resolver import Resolver


class Window(Widget):
	def __init__(self, app):
		self.app = app
		if getattr(sys, 'frozen', False):
			# frozen
			self.path = os.path.dirname(sys.executable) + "/"
		else:
			# unfrozen
			self.path = os.path.dirname(os.path.realpath(__file__)) + "/"
		super(Window, self).__init__()
	### OLD INTERFACE: ###
		# self.interface = old_Interface(self)
	### NEW INTERFACE: ###
		self.interface = Interface(self)
		self.resolver = Resolver(self)

	def resolve_sudoku(self, sudoku):
		try:
			start_new_thread(self.resolver.startSolvingSudoku, (sudoku,))
		except:
			self.interface.resolved(False, sudoku)

	def exitApp(self):
		self.app.exit()


class SudokuSolver(App):
	def build(self):
		self.title = "Sudoku Solver"
		self.window = Window(self)
		# return self.window
		return self.window.interface

	def exit(self):
		self.get_running_app().stop()

	# def on_stop(self):
	# 	print("STOP APP!!!")


if __name__ == "__main__":
	SudokuSolver().run()
