# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 17:08:31 2019

@author: Patrick
"""

import requests
import json
import os
import objectpath

from requests.auth import HTTPBasicAuth #Mengambil fungsi HTTPBasicAuth dari requests
    
def checkHost(controllerIP):
    #URL untuk REST get
    URL = 'http://'+controllerIP+':8181/restconf/operational/opendaylight-inventory:nodes'
    
    fileOldExist = False
    fileNewExist = False
    if (os.path.isfile('dataNodesNew.json')):
        fileNewExist = True
    
    if (os.path.isfile('dataNodesOld.json')):
        fileOldExist = True
    
    if fileOldExist:
        os.remove("dataNodesOld.json")
    
    if fileNewExist:
        os.rename('dataNodesNew.json','dataNodesOld.json')

    response = requests.get(URL, auth = HTTPBasicAuth('admin','admin'))
    
    print(response.status_code)
    
    response.json()
    
    with open('dataNodesNew.json','w') as outfile:
        json.dump(response.json(),outfile,sort_keys=True,indent=4)

    if fileNewExist:
        with open('dataNodesNew.json') as new:
            dataNew = json.load(new)
            print ('finish Load New')

    if fileOldExist:
        with open('dataNodesOld.json') as old:
            dataOld = json.load(old)
            print ('finish Load Old')

    checkUpdate = False
    
    if ('node' in dataNew['nodes']):
        countNodesNew = len(dataNew['nodes']['node']) #count how many nodes are there
        for nodes in range (0,countNodesNew):
            countNodeConnectedNew = len(dataNew['nodes']['node'][nodes]['node-connector'])
            for x in range (0,countNodeConnectedNew):
                if ('address-tracker:addresses' in dataNew['nodes']['node'][nodes]['node-connector'][x]):
                    countAddressNew = len(dataNew['nodes']['node'][nodes]['node-connector'][x]['address-tracker:addresses'])
                    
                    portName = dataNew['nodes']['node'][nodes]['node-connector'][x]['flow-node-inventory:name']
                    
                    if (('node' in dataOld['nodes']) and ('node' in dataNew['nodes'])):
                        jsonnn_tree_old = objectpath.Tree(dataOld['nodes']['node'][nodes])
                        a="$.'node-connector'[@.'flow-node-inventory:name' is '"+portName+"'].'address-tracker:addresses'"
                        oldAddress = list(jsonnn_tree_old.execute(a))
                        
                        if not oldAddress:
                            countAddressOld = 0
                        else:
                            countAddressOld = len(oldAddress[0])
                            
        
                        if countAddressNew != countAddressOld:
                            checkUpdate = True
                            break
                else:
                    countAddressNew = 0
                                                
                    portName = dataNew['nodes']['node'][nodes]['node-connector'][x]['flow-node-inventory:name']
                    
                    if (('node' in dataOld['nodes']) and ('node' in dataNew['nodes'])):
                        jsonnn_tree_old = objectpath.Tree(dataOld['nodes']['node'][nodes])
                        a="$.'node-connector'[@.'flow-node-inventory:name' is '"+portName+"'].'address-tracker:addresses'"
                        oldAddress = list(jsonnn_tree_old.execute(a))
                        
                        if not oldAddress:
                            countAddressOld = 0
                        else:
                            countAddressOld = len(oldAddress[0])
                            
                        if countAddressNew != countAddressOld:
                                checkUpdate = True
                                break
                        
    return checkUpdate

def countNodes():
    countNodesNew = 0
    fileNewExist = False
    if (os.path.isfile('dataNodesNew.json')):
        fileNewExist = True
    
    if (fileNewExist) :
        with open('dataNodesNew.json') as new:
                dataNew = json.load(new)
                print ('finish Load New')
        
        countNodesNew = len(dataNew['nodes']) #count how many nodes are there
        
    return countNodesNew
