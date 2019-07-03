# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 15:34:42 2019
['python ', 'objectpathtesttk.py']
@author: User
"""

import uuidswitch
import reactiveFlow
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from requests.auth import HTTPBasicAuth
import os
from subprocess import Popen, PIPE, call


dirpath = os.getcwd()

running = False
file = dirpath+'/objectpathtesttk.py'

def reactiveflow():
    os.system('"' + file + '"')
    os.system('"python ' + file + '"')
    
    
def objectpathtestMAIN():
    os.system('"python ' + file + '"')
    
    
def start():
    """Enable scanning by setting the global flag to True."""
    global running
    global controllerIP
    controllerIP=simpledialog.askstring("input Controller ip","please enter Controller ip")
    running = True

def stop():
    """Stop scanning by setting the global flag to False."""
    global running
    running = False
    
def scanning():
    if running:  # Only do this if the Stop button has not been clicked
        reactiveFlow.reactive(controllerIP)

    # After 1 second, call scanning again (create a recursive loop)
    window.after(6000, scanning) 

window=Tk()
window.title("MAIN") 
btn2= Button(window, text="   Run Reactive Flow   ",command=start)
btn2.pack(pady=15,ipady=2,)
btn4= Button(window, text="   Stop Reactive Flow   ",command=stop)
btn4.pack(pady=15,ipady=2)
btn = Button(window, text="      OVSDB Toolbar      ",command=uuidswitch.callovsdb)
btn.pack(pady=15,ipady=2)
btn3= Button(window, text="   OpenFlow Version   ",command=objectpathtestMAIN)
btn3.pack(pady=15,ipady=2)
window.geometry('200x250')
window.after(500, scanning)  # After 1 second, call scanning
window.mainloop()