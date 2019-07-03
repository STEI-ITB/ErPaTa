# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 17:08:31 2019

@author: Patrick
"""


import putFlow
import createFlow
import time
import checkHost
import delFlow
import tkinter

from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from requests.auth import HTTPBasicAuth

def reactive(controllerIP):  
    if (checkHost.countNodes() == 0):
        delFlow.delFlow(controllerIP)
    if checkHost.checkHost(controllerIP):
        print('New Update')
        delFlow.delFlow(controllerIP)
        createFlow.createFlowMultiSubnet()
        putFlow.putFlow(controllerIP)


    

