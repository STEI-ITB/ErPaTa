#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:21:41 2019

@author: fica
"""

import requests
import json
import objectpath
import tkinter
from requests.auth import HTTPBasicAuth
from tkinter import Label, Entry, Frame, Radiobutton, Button, messagebox


def inputflow(filename,ipctr,idopt,flownum):
    global response
    
    URL = 'http://'+str(ipctr)+':8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:'+str(idopt)
    putURL = 'http://'+str(ipctr)+':8181/restconf/config/opendaylight-inventory:nodes/node/openflow:'+str(idopt)+'/table/100/flow/'+str(flownum)
        
    dataFlow1 = filename
        
    headers = {'Accept':'application/xml','Content-type':'text/xml'}
        
    with open(dataFlow1) as fh:
        mydata = fh.read()
        responsePut = requests.put(putURL,
                                   data=mydata,
                                   auth=HTTPBasicAuth('admin','admin'),
                                   headers=headers,
                                   )
        print('Put:'+str(responsePut.status_code))    
        
    response = requests.get(URL, auth = HTTPBasicAuth('admin','admin'))
    
    print('Get:'+str(response.status_code))
    
    response.json()
        

def callback():
    ip_opt = ip_ctr.get()
    flow_opt = flow.get()
    id_opt = id_sw.get()
    
    print("a"+ip_opt)
    if flow_opt == 1:
        inputflow('dataFlowNormal.xml',ip_opt,id_opt,1)
    else:
        inputflow('dataFlow1.xml',ip_opt,id_opt,1)
        inputflow('dataFlow2.xml',ip_opt,id_opt,2)
    
    with open('dataflowversion.json','w') as outfile:
        json.dump(response.json(),outfile,sort_keys=True,indent=4) 
    
    with open("dataflowversion.json") as fh:
        data = json.load(fh)
    
    tree = objectpath.Tree(data['node'][0])
    
    
    idtable = "$.'flow-node-inventory:table'[@.'id' is 100].'flow'"
    
    listtable = list(tree.execute(idtable))
    print (listtable)
    
    if (listtable == []):
        messagebox.showinfo("OpenFlow Version","OpenFlow 1.0")
    else:
        messagebox.showinfo("OpenFlow Version","OpenFlow 1.3")
    

    

def lala():
    global ip_ctr
    global id_sw
    global flow
    
    widget = tkinter.Tk()
    widget.title("OpenFlow Version")
    flow = tkinter.IntVar()
    ip_ctr = tkinter.StringVar()
    id_sw = tkinter.StringVar()
    width = 280
    height = 250
    screen_width= widget.winfo_screenwidth()
    screen_height = widget.winfo_screenheight()
    
    x_coordinate = (screen_width/2) - (width/2)
    y_coordinate = (screen_height/2) - (height/2)
    
    MyFrame = Frame(widget, height=250, width=280)
    
    Label(widget, text="IP Controller").place(x=10,y=10,height=35)
    Entry(widget, width=20, textvariable=ip_ctr).place(x=100,y=10,height=35)
    Label(widget, text="ID Switch").place(x=10,y=50,height=35)
    Entry(widget, width=20, textvariable=id_sw).place(x=100,y=50,height=35)
    
    Label(widget, text="Jenis Flow").place(x=10,y=90,height=35)
    Radiobutton(widget,text="Normal",variable=flow,value=1).place(x=100,y=90,height=35) 
    Radiobutton(widget,text="Inport",variable=flow,value=2).place(x=180,y=90,height=35)
    
    Button(widget, text="Ok", command=callback, bd=2).place(x=120,y=130,height=35)
    
    MyFrame.pack()
    widget.geometry("%dx%d+%d+%d" % (width, height, x_coordinate, y_coordinate))
    widget.mainloop()   
#Tkinter program
lala()