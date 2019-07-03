# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 21:32:35 2019

2d6db786-0708-4110-8ab2-c89d388004fe

@author: eric
"""
# Example
import json
import requests
import urllib.parse
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from requests.auth import HTTPBasicAuth


uuid=""
ip=""
data = {}
databridge = {}
dataport = {}
datacheckconnection={}
path = ''
fileName ='activeconnection'
fileNameBridge ='bridge'
fileNamePort ='port'
def get_data(): 
    global uuid
    global ip
    global data
    global putURLconnection
    ip=simpledialog.askstring("Input Manager ip","            Please enter Manager ip            ")
    uuid=simpledialog.askstring("Input Switch uuid","                              Please enter uuid                              ")
    print(uuid)
    ipswitch=simpledialog.askstring("Input Switch ip", "            Please enter Switch ip            ")
    print(ipswitch)
    data = {
            "network-topology:node": [
                {
                    "node-id": "ovsdb://uuid/"+uuid,
                    "connection-info": {
                                        "ovsdb:remote-port": "6640",
                                        "ovsdb:remote-ip": ipswitch
                                       }
                }
              ]
            }
    putURLconnection='http://' + ip + ':8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2Fuuid%2F'+uuid
    print(putURLconnection)
    writeToJSONFile(path,fileName,data)
    
def getconnectionapi():
    global datacheckconnection
    urlget = 'http://'+ip+':8181/restconf/operational/network-topology:network-topology/topology/ovsdb:1/'
    response = requests.get(urlget, auth = HTTPBasicAuth('admin','admin'))
    print(response.status_code)
    response.json()
    with open('data.json','w') as outfile:
        json.dump(response.json(),outfile,sort_keys=True,indent=4) 
    datacheckconnection=response.json()

def checkconnection():
    getconnectionapi()
    for here in datacheckconnection['topology']:
        if 'node' not in here:
            messagebox.showerror("Error", "Not Connected")
        else:
            messagebox.showinfo("Information","Connected")    
            
def checkresult(hasil):
     branchcheck = Tk()
     branchcheck.title('Result')
     Label3= Label(branchcheck, text=hasil,    font = ('Calibri' , 20), fg = 'black', width = 11, height = 2, borderwidth = 1, relief = 'solid')
     Label3.pack()
     branchcheck.geometry("200x200")
     branchcheck.mainloop()
    
        
def writeToJSONFile(path, fileName, data):
    filePathNameWExt = path + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp , sort_keys=True,indent=4) 
            

def initiateconnection():
    dataconnection = 'activeconnection.json'
    headers = {'Accept':'application/json','Content-type':'application/json'}
    with open(dataconnection) as fh:
        mydata = fh.read()
        responsePut = requests.put(putURLconnection,
                               data=mydata,
                               auth=HTTPBasicAuth('admin','admin'),
                               headers=headers,
                               )
    print(responsePut.status_code)
    #checkresult(responsePut.status_code)
     
   
def addbridge():
    global databridge
    global putURLbridge
    bridge=simpledialog.askstring("input bridge name","please enter bridge name")
    ipcontroller=simpledialog.askstring("input Controller ip","please enter Controller ip")
    print(bridge)
    databridge={
    "network-topology:node": [
        {
          "node-id": "ovsdb://uuid/"+uuid+"/bridge/"+bridge,
             "ovsdb:bridge-name": bridge,
             "ovsdb:protocol-entry": [
        		{
        			"protocol": "ovsdb:ovsdb-bridge-protocol-openflow-13"
        		}
        	   ],
              "ovsdb:controller-entry": [
                {
                  "target": "tcp:" + ipcontroller + ":6633"
                }
              ],
             "ovsdb:managed-by": "/network-topology:network-topology/network-topology:topology[network-topology:topology-id='ovsdb:1']/network-topology:node[network-topology:node-id='ovsdb://uuid/"+ uuid +"']"
             }
        ]
    }
    putURLbridge='http://'+ip+':8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2Fuuid%2F'+uuid+'%2Fbridge%2F'+ bridge
    

def sendbridge():
    dataconnection = 'bridge.json'
    headers = {'Accept':'application/json','Content-type':'application/json'}
    with open(dataconnection) as fh:
        mydata = fh.read()
        responsePut = requests.put(putURLbridge,
                               data=mydata,
                               auth=HTTPBasicAuth('admin','admin'),
                               headers=headers,
                               )
    print(responsePut.status_code)
    #checkresult(responsePut.status_code)
    
def combinebridge():
    addbridge()
    writeToJSONFile(path,fileNameBridge,databridge)
    sendbridge()
    
def addport():
    global dataport
    global putURLport
    bridge=simpledialog.askstring("input bridge name","please enter bridge name you want to add port")
    portname=simpledialog.askstring("input port name","please enter port name")
    portnumber=simpledialog.askstring("input port number","please enter port number")
    portnameencode=urllib.parse.quote(portname,safe ='')
    print(portnameencode)
    dataport={
    "network-topology:termination-point": [
            {
            "tp-id": portname,
            "ovsdb:ofport": portnumber,
            "ovsdb:name": portname
            }
        ]
    }
    putURLport='http://'+ip+':8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2Fuuid%2F'+uuid+'%2Fbridge%2F'+bridge+'/termination-point/'+portnameencode
    print(putURLport)
    

def sendport():
    dataconnection = 'port.json'
    headers = {'Accept':'application/json','Content-type':'application/json'}
    with open(dataconnection) as fh:
        mydata = fh.read()
        responsePut = requests.put(putURLport,
                               data=mydata,
                               auth=HTTPBasicAuth('admin','admin'),
                               headers=headers,
                               )
    print(responsePut.status_code)
    #checkresult(responsePut.status_code)    

def combineport():
    addport()
    writeToJSONFile(path,fileNamePort,dataport)
    sendport()
    
def deletebridge():
    global deleteURL
    bridge=simpledialog.askstring("Input bridge name you want to delete","Input bridge name you want to delete")
    deleteURL='http://'+ip+':8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2Fuuid%2F'+uuid+'%2Fbridge%2F'+ bridge
    print(bridge)
    print(deleteURL)

def deleteapi():
    payload={'some':'data'}
    headers = {'Accept':'application/json','Content-type':'application/json'}
    response = requests.delete(deleteURL, data=json.dumps(payload), headers=headers,auth=HTTPBasicAuth('admin', 'admin'))
    print(response.status_code)
    #checkresult(response.status_code)
    
def combinedelbridge():
    deletebridge()
    deleteapi()
    
def deleteport():
    global deleteURL
    bridge=simpledialog.askstring("Input bridge name where port is located","Input bridge name where is port located")
    portname=simpledialog.askstring("input port name","please enter port name")
    portnameencode=urllib.parse.quote(portname,safe ='')
    deleteURL='http://'+ip+':8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2Fuuid%2F'+uuid+'%2Fbridge%2F'+ bridge+'/termination-point/'+portnameencode
    print(bridge)
    print(deleteURL)

def combinedelport():
    deleteport()
    deleteapi()

def terminateconnection():
    terminateurl='http://' + ip + ':8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2Fuuid%2F'+uuid
    payload={'some':'data'}

    headers = {'Accept':'application/json','Content-type':'application/json'}

    response = requests.delete(terminateurl, data=json.dumps(payload), headers=headers,auth=HTTPBasicAuth('admin', 'admin'))
    print(response.status_code)
    #checkresult(response.status_code)
 
def delete():
    branch = Tk()
    branch.title('Choose what you want to delete?')
    button8= Button(branch, text="              Delete Bridge              ",command=combinedelbridge)
    button8.pack(pady=10,ipady=2)
    button9= Button(branch, text="                Delete Port                ",command=combinedelport)
    button9.pack(pady=10,ipady=2)
    branch.geometry("400x100")
    branch.mainloop()
    
def callovsdb():
    root = Tk()
    width = 300
    height = 400
    screen_width= root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x_coordinate = (screen_width/2) - (width/2)
    y_coordinate = (screen_height/2) - (height/2)
    root.title('OVSDB ToolBar')   
    button = Button(root, text=" Input Manager IP and Switch UUID & IP ",command=get_data)
    button.pack(pady=10,ipady=2)
    button2= Button(root, text="           Initiate Active Connection             ",command=initiateconnection)
    button2.pack(pady=10,ipady=2)
    button3= Button(root, text="                 Check Connection                   ",command=checkconnection)
    button3.pack(pady=10,ipady=2)
    button4= Button(root, text="              Terminate Connection                ",command=terminateconnection)
    button4.pack(pady=10,ipady=2)
    button5= Button(root, text="                         Add-Bridge                         ",command=combinebridge)
    button5.pack(pady=10,ipady=2)
    button6= Button(root, text="                           Add-Port                           ",command=combineport)
    button6.pack(pady=10,ipady=2)
    button7= Button(root, text="                 Delete Bridge or Port                 ",command=delete)
    button7.pack(pady=10,ipady=2)
    label1 = Label(root, text = "author : eric_angwyn")
    label1.pack(side=RIGHT)
    root.geometry("%dx%d+%d+%d" % (width, height, x_coordinate, y_coordinate))
    root.mainloop()
    