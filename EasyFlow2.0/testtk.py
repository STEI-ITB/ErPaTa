# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 10:51:10 2019

@author: 
"""

import requests
import tkinter

from requests.auth import HTTPBasicAuth
from tkinter import Label, Entry, Frame, Radiobutton, Button, messagebox

def table_edit(filename,tablenum):
    if tablenum == 100:
        with open(filename) as f:
            newText=f.read().replace('<table_id>0','<table_id>100')
            
        with open(filename,'w') as f:
            f.write(newText)
    else:
        with open(filename) as f:
            newText=f.read().replace('<table_id>100','<table_id>0')
            
        with open(filename,'w') as f:
            f.write(newText)
    return

def inputflow(filename,ipctr,idopt,tableid,flownum):
    URL = 'http://'+str(ipctr)+':8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:'+str(idopt)+'/table/'+str(tableid)
    putURL = 'http://'+str(ipctr)+':8181/restconf/config/opendaylight-inventory:nodes/node/openflow:'+str(idopt)+'/table/'+str(tableid)+'/flow/'+str(flownum)
        
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
        
        messagebox.showinfo("Notification",str(response.status_code))


def callback():
    ip_opt = ip_ctr.get()
    id_opt = id_sw.get()
    flow_opt = flow.get()
    aruba_opt = aruba.get()
    
    if aruba_opt == 1:
        table_id = 100
    else:
        table_id = 0
        
    table_edit('dataFlowNormal.xml',table_id)
    table_edit('dataFlow1.xml',table_id)
    table_edit('dataFlow2.xml',table_id)
    
    if flow_opt == 1:
        inputflow('dataFlowNormal.xml',ip_opt,id_opt,table_id,1)
    else:
        inputflow('dataFlow1.xml',ip_opt,id_opt,table_id,1)
        inputflow('dataFlow2.xml',ip_opt,id_opt,table_id,2)

#Tkinter program
def testtk():
    widget = tkinter.Tk()
    widget.title("Input Flow Entries")
    width = 280
    height = 250
    screen_width= widget.winfo_screenwidth()
    screen_height = widget.winfo_screenheight()
    
    x_coordinate = (screen_width/2) - (width/2)
    y_coordinate = (screen_height/2) - (height/2)
    flow = tkinter.IntVar()
    aruba = tkinter.IntVar()
    ip_ctr = tkinter.StringVar()
    id_sw = tkinter.StringVar()
    
    MyFrame = Frame(widget, height=250, width=280)
    
    Label(widget, text="IP Controller").place(x=10,y=10,height=35)
    Entry(widget, width=20, textvariable=ip_ctr).place(x=100,y=10,height=35)
    
    Label(widget, text="ID Switch").place(x=10,y=50,height=35)
    Entry(widget, width=20, textvariable=id_sw).place(x=100,y=50,height=35)
    
    Label(widget, text="Jenis Flow").place(x=10,y=90,height=35)
    Radiobutton(widget,text="Normal",variable=flow,value=1).place(x=100,y=90,height=35) 
    Radiobutton(widget,text="Inport",variable=flow,value=2).place(x=180,y=90,height=35)
    
    Label(widget, text="Switch Aruba").place(x=10,y=130,height=35)
    Radiobutton(widget,text="Yes",variable=aruba,value=1).place(x=100,y=130,height=35) 
    Radiobutton(widget,text="No",variable=aruba,value=2).place(x=180,y=130,height=35)
    
    Button(widget, text="OK", command=callback, bd=2).place(x=120,y=90,height=35)
    
    MyFrame.pack()
    widget.geometry("%dx%d+%d+%d" % (width, height, x_coordinate, y_coordinate))
    widget.mainloop()


#responsePut = requests.put(putURL,auth=HTTPBasicAuth('admin','admin'),headers=headers, data=dataFlow1)
