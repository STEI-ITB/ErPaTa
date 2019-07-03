# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 03:48:35 2019

@author: User
"""

from tkinter import *
window = Tk()
variable = "data"

def changeVariable():
    global variable
    variable = "different data"

def printVariable():
    print(variable)

button1 = Button(window, command = changeVariable)
button1.pack()
button2 = Button(window, command = printVariable)
button2.pack()

window.mainloop()