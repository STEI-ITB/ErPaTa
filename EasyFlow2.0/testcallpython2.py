# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:48:51 2019

@author: User
"""
import json
import tkinter
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox

from requests.auth import HTTPBasicAuth
def dia():
    controllerIP = ip.get()
    while True:
        print(controllerIP)
        
reactivewindow = tkinter.Tk()
reactivewindow.title("Input IP Controller")

ip = tkinter.StringVar()


MyFrame = Frame(reactivewindow, height=250, width=280)

Label(reactivewindow, text="IP Controller").place(x=10,y=50,height=35)
Entry(reactivewindow, width=20, textvariable=ip).place(x=100,y=50,height=35)

Button(reactivewindow, text="OK", command=dia, bd=2).place(x=120,y=180,height=35)

MyFrame.pack()
reactivewindow.mainloop()



        
