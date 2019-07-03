# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 10:51:10 2019

@author: Patrick
"""

import requests
import os
import json

from requests.auth import HTTPBasicAuth #Mengambil fungsi HTTPBasicAuth dari requests

def putFlow(controllerIP):

    with open('dataNodesNew.json') as fh:
        data = json.load(fh)
    
    countNodes = len(data['nodes']['node'])
    
    #static FLOW
    for nodes in range (1,countNodes):
        payload = {'some':'data'}
        headersDel = {'content-type': 'application/xml'}
        delUrl = "http://"+controllerIP+":8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+str(nodes)
        response = requests.delete(delUrl, data=json.dumps(payload), headers=headersDel,auth=HTTPBasicAuth('admin','admin'))
        print(response.status_code)
        
    #URL untuk REST put
    for nodes in range (0,countNodes):
        
        nodeID = data['nodes']['node'][nodes]['id']
    
        countNodeConnected = len(data['nodes']['node'][nodes]['node-connector'])
        nodeIDName = nodeID.replace('openflow:','S')
        
        idNum = 0
        
        for y in range (9998,10000):
            putURLStatic= 'http://'+controllerIP+':8181/restconf/config/opendaylight-inventory:nodes/node/'+nodeID+'/table/1/flow/'+str(y)
            dataFlowS= 'dataFlowS'+str(y)+'.json'
            headers = {'Accept':'application/json','Content-type':'application/json'}
            with open(dataFlowS) as fh:
                mydata = fh.read()
                responsePut = requests.put(putURLStatic,
                                           data=mydata,
                                           auth=HTTPBasicAuth('admin','admin'),
                                           headers=headers,
                                           )
                print(responsePut.status_code)
        
        for x in range (0,countNodeConnected):
            connectorConfiguration = data['nodes']['node'][nodes]['node-connector'][x]['flow-node-inventory:configuration']
            if (connectorConfiguration != 'PORT-DOWN'):
                if ('address-tracker:addresses' in data['nodes']['node'][nodes]['node-connector'][x]):
                    countAddress = len(data['nodes']['node'][nodes]['node-connector'][x]['address-tracker:addresses'])
                    for address in range (0,countAddress):
                        putURLIP = 'http://'+controllerIP+':8181/restconf/config/opendaylight-inventory:nodes/node/'+nodeID+'/table/20/flow/'+str(idNum)
                        putURLARP = 'http://'+controllerIP+':8181/restconf/config/opendaylight-inventory:nodes/node/'+nodeID+'/table/1/flow/'+str(idNum+200)
                        putURLL3 = 'http://'+controllerIP+':8181/restconf/config/opendaylight-inventory:nodes/node/'+nodeID+'/table/1/flow/'+str(idNum+100)
                        putURLARPGw = 'http://'+controllerIP+':8181/restconf/config/opendaylight-inventory:nodes/node/'+nodeID+'/table/10/flow/'+str(idNum)
                        putURLL2 = 'http://'+controllerIP+':8181/restconf/config/opendaylight-inventory:nodes/node/'+nodeID+'/table/1/flow/'+str(idNum)
                        putURLRegistrasi = 'http://'+controllerIP+':8181/restconf/config/opendaylight-inventory:nodes/node/'+nodeID+'/table/0/flow/'+str(idNum)
                        putURLARPL2 = 'http://'+controllerIP+':8181/restconf/config/opendaylight-inventory:nodes/node/'+nodeID+'/table/30/flow/'+str(idNum)
                        
                        dataFlowIP = 'dataFlowIP/dataFlowIP'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json'
                        dataFlowARP = 'dataFlowARP/dataFlowARP'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json'
                        dataFlowL3 = 'dataFlowL3/dataFlowL3'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json'
                        dataFlowARPGw = 'dataFlowARPGw/dataFlowARPGw'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json'
                        dataFlowL2 = 'dataFlowL2/dataFlowL2'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json'
                        dataFlowRegistrasi = 'dataFlowRegistrasi/dataFlowRegistrasi'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json'
                        dataFlowARPL2 = 'dataFlowARPL2/dataFlowARPL2'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json'
                        
                        headers = {'Accept':'application/json','Content-type':'application/json'}
                        
                        checkPut = False
                        
                        if (os.path.isfile(dataFlowIP)):
                            with open(dataFlowIP) as fh:
                                mydata = fh.read()
                                responsePut = requests.put(putURLIP,
                                                           data=mydata,
                                                           auth=HTTPBasicAuth('admin','admin'),
                                                           headers=headers,
                                                           )
                                print('dataFlowIP'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json : '+str(responsePut.status_code)+' - idNum: '+str(idNum))
                                checkPut = True
                                
                        if (os.path.isfile(dataFlowARP)):
                            with open(dataFlowARP) as fh:
                                mydata = fh.read()
                                responsePut = requests.put(putURLARP,
                                                           data=mydata,
                                                           auth=HTTPBasicAuth('admin','admin'),
                                                           headers=headers,
                                                           )
                                print('dataFlowARP'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json : '+str(responsePut.status_code)+' - idNum: '+str(idNum))
                                checkPut = True
                            
                        if (os.path.isfile(dataFlowL3)):
                            with open(dataFlowL3) as fh:
                                mydata = fh.read()
                                responsePut = requests.put(putURLL3,
                                                           data=mydata,
                                                           auth=HTTPBasicAuth('admin','admin'),
                                                           headers=headers,
                                                           )
                                print('dataFlowL3'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json : '+str(responsePut.status_code)+' - idNum: '+str(idNum))
                                checkPut = True
                                                        
                        if (os.path.isfile(dataFlowARPGw)):
                            with open(dataFlowARPGw) as fh:
                                mydata = fh.read()
                                responsePut = requests.put(putURLARPGw,
                                                           data=mydata,
                                                           auth=HTTPBasicAuth('admin','admin'),
                                                           headers=headers,
                                                           )
                                print('dataFlowARPGw'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json : '+str(responsePut.status_code)+' - idNum: '+str(idNum))
                                checkPut = True
                                
                        if (os.path.isfile(dataFlowL2)):
                            with open(dataFlowL2) as fh:
                                mydata = fh.read()
                                responsePut = requests.put(putURLL2,
                                                           data=mydata,
                                                           auth=HTTPBasicAuth('admin','admin'),
                                                           headers=headers,
                                                           )
                                print('dataFlowL2'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json : '+str(responsePut.status_code)+' - idNum: '+str(idNum))
                                checkPut = True
                            
                        if (os.path.isfile(dataFlowRegistrasi)):
                            with open(dataFlowRegistrasi) as fh:
                                mydata = fh.read()
                                responsePut = requests.put(putURLRegistrasi,
                                                           data=mydata,
                                                           auth=HTTPBasicAuth('admin','admin'),
                                                           headers=headers,
                                                           )
                                print('dataFlowRegistrasi'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json : '+str(responsePut.status_code)+' - idNum: '+str(idNum))
                                checkPut = True
                        
                        if (os.path.isfile(dataFlowARPL2)):
                            with open(dataFlowARPL2) as fh:
                                mydata = fh.read()
                                responsePut = requests.put(putURLARPL2,
                                                           data=mydata,
                                                           auth=HTTPBasicAuth('admin','admin'),
                                                           headers=headers,
                                                           )
                                print('dataFlowARPL2'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json : '+str(responsePut.status_code)+' - idNum: '+str(idNum))
                                checkPut = True
                        
                        if (checkPut):
                            idNum=idNum+1