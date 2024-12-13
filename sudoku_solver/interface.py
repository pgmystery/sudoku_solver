# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup


class Interface(BoxLayout):
	def __init__(self, main):
		self.main = main
		super(Interface, self).__init__()
		self.numberButtons = []
		for gridField in self.ids["sudokuFieldLayout"].children:
			self.numberButtons.extend(gridField.children[0].children)
		self.numberSelectPopup = NumberSelectPopup(self)
		self.resolvePopup = ResolvePopup()
		self.selectedButton = None
		self.resolving = False

	def numberButtonRelease(self, btn):
		self.selectedButton = btn
		self.numberSelectPopup.open(self.selectedButton.text)

	def numberSelectButtonRelease(self, btn):
		if btn.text.lower() == "reset":
			self.selectedButton.text = "X"
		else:
			self.selectedButton.text = btn.text
		self.numberSelectPopup.dismiss()

	def numberSelectButtonTouchDown(self, btn):
		if self.selectedButton.text == btn.text:
			return

	def numberSelectButtonTouchUp(self, btn):
		if self.selectedButton.text != btn.text:
			btn.state = "normal"

	def resolve(self):
		if self.resolving:
			return
		self.resolving = True
		self.resolvePopup.open()
		sudoku = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
		]
		for button in self.numberButtons:
			if button.text.lower() == "x":
				text = 0
			else:
				text = int(button.text)
			sudoku[int(button.gridId[0])][int(button.gridId[1])] = text
		self.main.resolve_sudoku(sudoku)

	def resolved(self, result, sudoku):
		if result:
			for button in self.numberButtons:
				text = sudoku[int(button.gridId[0])][int(button.gridId[1])]
				if text == 0:
					text = "X"
				button.text = str(text)
		self.resolving = False
		self.resolvePopup.dismiss()

	def clear(self):
		for button in self.numberButtons:
			button.text = "X"


class NumberSelecterButton(ToggleButton):
	def __init__(self, *args, **kwargs):
		super(NumberSelecterButton, self).__init__(*args, **kwargs)

	def on_touch_down(self, touch):
		if self.interface.selectedButton.text == self.text:
			return
		super(NumberSelecterButton, self).on_touch_down(touch)

	def on_touch_up(self, touch):
		if self.interface.selectedButton.text != self.text:
			self.state = "normal"
		super(NumberSelecterButton, self).on_touch_up(touch)



class NumberSelectPopup(Popup):
	def __init__(self, interface):
		self.interface = interface
		super(NumberSelectPopup, self).__init__()
		self.buttons = self.ids["buttonGrid"].children

	def open(self, buttonText):
		for button in self.buttons:
			if button.text == buttonText:
				button.state = "down"
			else:
				button.state = "normal"
		super(NumberSelectPopup, self).open()


class ResolvePopup(Popup):
	def __init__(self):
		super(ResolvePopup, self).__init__()
