# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:10:38 2019

@author: Patrick
"""
import json
import objectpath
import shutil
import os

def createFlowMultiSubnet():
    dirpath = os.getcwd()
    def num_to_directory(argument):
        switcher = {
                0:dirpath+'/dataFlowARPGw',
                1:dirpath+'/dataFlowARP',
                2:dirpath+'/dataFlowIP',
                3:dirpath+'/dataFlowL2',
                4:dirpath+'/dataFlowL3',
                5:dirpath+'/dataFlowRegistrasi',
                6:dirpath+'/dataFlowARPL2'
                }
        return switcher.get(argument,'false')
    
    for countDir in range(0,7):        
        directory = num_to_directory(countDir)
        if os.path.exists(directory):
            shutil.rmtree(directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
    with open('dataNodesNew.json') as fh:
        data = json.load(fh) #get file json Nodes
    
    countNodes = len(data['nodes']['node']) #count how many nodes are there
    print (countNodes)
    
    for nodes in range (0,countNodes): #loop for the amount of switch is connected to the controller
        countNodeConnected = len(data['nodes']['node'][nodes]['node-connector']) #count how many ports are on the switch
        print (countNodeConnected)
    
        idNum = 0 #ID for the flow
    
        nodeID = data['nodes']['node'][nodes]['id'] #get the ID of the switch
        print (nodeID)
        nodeIDName = nodeID.replace('openflow:','S') #this is used for the file name for each flow, to identify each flow for which switch ID
        print (nodeIDName)
        for x in range (0,countNodeConnected): #loop for the amount of ports there are on one switch
    
            connectorConfiguration = data['nodes']['node'][nodes]['node-connector'][x]['flow-node-inventory:configuration'] #this is to detect the port is down or not
            if (connectorConfiguration != 'PORT-DOWN'): #if the port is not down, then we create the flow
                
                if ('address-tracker:addresses' in data['nodes']['node'][nodes]['node-connector'][x]):
                    jsonnn_tree = objectpath.Tree(data['nodes']['node'][nodes]['node-connector'][x])
                    c="$.'address-tracker:addresses'.ip" #this is the location in the json file for IP address from each devices that connected to the switch
                    result_IP = tuple (jsonnn_tree.execute(c)) #get all IP address from the json file and make it as tuple
                    
                    countAddress = len(data['nodes']['node'][nodes]['node-connector'][x]['address-tracker:addresses']) #count how many devices is connected to the switch on one port
                    print ('Number of Devices : '+str(countAddress))
                    for address in range (0,countAddress): #loop for the amount of the devices
                        IP=''.join(result_IP[address]) #IP address of a single device is assign as string for each loop. This is used to get the mac address and the port number of the switch for that IP address
                        print(IP)
                        a="$.'address-tracker:addresses'[@.'ip' is '"+IP+"'].mac" #get the mac address for the specific IP address
                        nodeConnector = data['nodes']['node'][nodes]['node-connector'][x]['flow-node-inventory:port-number'] #get the port number for the specific IP address
                        hardwareAddress = data['nodes']['node'][nodes]['node-connector'][x]['flow-node-inventory:hardware-address']
                        result_tuple1 = tuple(jsonnn_tree.execute(a))
                        print (result_tuple1)
                        macAddress= ''.join(result_tuple1) 
                        print (macAddress)
                        print('Connected to Port : '+ str(nodeConnector))
                        
                        IParray = IP.split('.') 
        
                        IParray [3] = '254'
                        
                        IPgw = '.'.join(IParray) #assuming the default gateway always ends with 254 (ex: 10.0.0.254)
                        
                        IParray [3] = '0'
                        
                        IPnet = '.'.join(IParray)
                                                
                        print ('Banyaknya node : ',countAddress)
                        if (countAddress==1):
                            #2nd Flow:
                            putJson = {
                                    "flow": [
                                    {
                                        "flow-name": "FlowS", 
                                        "id": idNum, 
                                        "instructions": {
                                            "instruction": [
                                            {
                                                "go-to-table": {
                                                    "table_id": 1
                                                }, 
                                                "order": 0
                                            }
                                            ]
                                        }, 
                                        "match": {
                                            "ethernet-match": {
                                                "ethernet-source":{
                                                    "address": macAddress
                                                }
                                            }
                                        },
                                        "priority": 100, 
                                        "table_id": 0
                                        }
                                    
                                    ]
                            }
                    
                            with open('dataFlowRegistrasi/dataFlowRegistrasi'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json','w') as outfile:
                                json.dump(putJson,outfile,sort_keys=True,indent=4)
                            
                            
                            #Creating the Flow:
                            #1st Flow:
                            putJson = { 
                            	"flow":[
                            		{	
                            			"id":idNum,
                            			"priority":10,
                            			"flow-name":"FlowIP"+str(x),
                            			"match": {
                            				"ethernet-match": {
                            					"ethernet-type":{
                            						"type":2048
                            					}
                            				},
                            				"ipv4-destination":IP+"/32"
                            			},
                            			"table_id":20,
                            			"instructions":{
                            				"instruction": [
                            					{
                            						"order":0,
                            						"apply-actions": {
                            							"action": [
                            								{
                            									"order": 0,
                            									"set-dl-dst-action": {
                            										"address":macAddress
                            									}
                            								},
                            								{
                            									"order":1,
                            									"output-action":{
                            										"output-node-connector": nodeConnector
                            									}
                            								}
                            							]	
                            						}
                            					}
                            				]
                            			}
                            		}
                            	]
                            }
                        
                            with open('dataFlowIP/dataFlowIP'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json','w') as outfile:
                                json.dump(putJson,outfile,sort_keys=True,indent=4) #make it as a file
                                                                                                                          
                            #2nd Flow:
                            putJson = {
                                    "flow": [
                                    {
                                        "flow-name": "FlowS", 
                                        "id": idNum+200, 
                                        "instructions": {
                                            "instruction": [
                                            {
                                                "go-to-table": {
                                                    "table_id": 10
                                                }, 
                                                "order": 0
                                            }
                                            ]
                                        }, 
                                        "match": {
                                            "ethernet-match": {
                                                "ethernet-type": {
                                                "type": 2054
                                                }
                                            },
                                            "arp-target-transport-address":IPgw+"/32"
                                        }, 
                                        "priority": 100, 
                                        "table_id": 1
                                    }]
                                    }
                    
                            with open('dataFlowARP/dataFlowARP'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json','w') as outfile:
                                json.dump(putJson,outfile,sort_keys=True,indent=4)
                            
                            #3rd Flow:
                            putJson = {
                                "flow":[
                            		{	
                            			"id":idNum,
                            			"priority":100,
                            			"flow-name":"FlowARP"+str(x),
                            			"match": {
                            				"ethernet-match": {
                            					"ethernet-type":{
                            						"type":2054
                            					}
                            				},
                            				"arp-target-transport-address":IPgw+"/32",
                            			},
                            			"table_id":10,
                            			"instructions":{
                            				"instruction": [
                            					{
                            						"order":0,
                            						"apply-actions": {
                            							"action": [
                            								 {
                                                        "openflowplugin-extension-nicira-action:nx-reg-move": {
                                                            "dst": {
                                                                "end": 47, 
                                                                "of-eth-dst": [
                                                                    None
                                                                ], 
                                                                "start": 0
                                                            }, 
                                                            "src": {
                                                                "end": 47, 
                                                                "of-eth-src": [
                                                                    None
                                                                ], 
                                                                "start": 0
                                                            }
                                                        }, 
                                                        "order": 0
                                                    }, 
                                                    {
                                                        "openflowplugin-extension-nicira-action:nx-reg-move": {
                                                            "dst": {
                                                                "end": 47, 
                                                                "nx-arp-tha": [
                                                                    None
                                                                ], 
                                                                "start": 0
                                                            }, 
                                                            "src": {
                                                                "end": 47, 
                                                                "nx-arp-sha": [
                                                                    None
                                                                ], 
                                                                "start": 0
                                                            }
                                                        }, 
                                                        "order": 1
                                                    }, 
                                                    {
                                                        "order": 2, 
                                                        "set-field": {
                                                            "arp-source-hardware-address": {
                                                                "address": hardwareAddress
                                                            }
                                                        }
                                                    }, 
                                                    {
                                                        "order": 3, 
                                                        "set-field": {
                                                            "arp-op": 2
                                                        }
                                                    }, 
                                                    {
                                                        "order": 4, 
                                                        "set-field": {
                                                            "ethernet-match": {
                                                                "ethernet-source": {
                                                                    "address": hardwareAddress
                                                                }
                                                            }
                                                        }
                                                    }, 
                                                    {
                                                        "openflowplugin-extension-nicira-action:nx-reg-move": {
                                                            "dst": {
                                                                "end": 31, 
                                                                "of-arp-tpa": [
                                                                    None
                                                                ], 
                                                                "start": 0
                                                            }, 
                                                            "src": {
                                                                "end": 31, 
                                                                "of-arp-spa": [
                                                                    None
                                                                ], 
                                                                "start": 0
                                                            }
                                                        }, 
                                                        "order": 5
                                                    }, 
                                                    {
                                                        "order": 6, 
                                                        "set-field": {
                                                            "arp-source-transport-address": IPgw+"/32"
                                                        }
                                                    }, 
                                                    {
                                                        "order": 7, 
                                                        "output-action": {
                                                            "max-length": 0, 
                                                            "output-node-connector": "IN_PORT"
                                                        }
                                                    }
                            							]
                            							
                            						}
                            					}
                            				]
                            			}
                            		}
                            	]
                            }
                    
                            with open('dataFlowARPGw/dataFlowARPGw'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json','w') as outfile:
                               json.dump(putJson,outfile,sort_keys=True,indent=4)
                               
                            #5th Flow
                            putJson = {
                                "flow":[
                            		{	
                            			"id":idNum+100,
                            			"priority":10,
                            			"flow-name":"FlowARP"+str(x),
                            			"match": {
                            				"ethernet-match": {
                                                "ethernet-type": {
                                                    "type": 2048
                                                }
                                            },
                                            "ipv4-destination": IP+"/32"
                                        },
                            			"table_id":1,
                            			"instructions":{
                            				"instruction": [
                            					{
                            						"order":0,
                            						"go-to-table":{
                                                        "table_id":20
                                                    }
                            					},
                                                {
                                                    "order": 1,
                                                    "apply-actions": {
                            							"action": [
                            								{
                            									"order": 0,
                            									"set-dl-src-action": {
                            										"address":hardwareAddress
                            									}                                             
                                                            },
                                                            {
                                                                "order": 1,   
                                                                "dec-nw-ttl": {}
                                                            }
                                                        ]
                                                    }
                                                }
                            				]
                            			}
                            		}
                            	]
                            }
                    
                            with open('dataFlowL3/dataFlowL3'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json','w') as outfile:
                               json.dump(putJson,outfile,sort_keys=True,indent=4)
                            

                            #4th Flow
                            putJson = {
                                        "flow": [
                                            {
                                                "flow-name": "FlowL2", 
                                                "id": idNum, 
                                                "instructions": {
                                                    "instruction": [
                                                        {
                                                            "go-to-table": {
                                                                "table_id": 20
                                                            }, 
                                                            "order": 0
                                                        }
                                                    ]
                                                }, 
                                                "match": {
                                                    "ethernet-match": {
                                                        "ethernet-type": {
                                                            "type": 2048
                                                        }
                                                    },
                                                    "ipv4-destination": IPnet+"/24",
                                                    "ipv4-source": IPnet+"/24"
                                                }, 
                                                "priority": 50, 
                                                "table_id": 1
                                            }
                                        ]
                                    }
                    
                            with open('dataFlowL2/dataFlowL2'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json','w') as outfile:
                               json.dump(putJson,outfile,sort_keys=True,indent=4)
                               
                            #4th Flow
                            putJson = {
                                        "flow": [
                                            {
                                                "flow-name": "FlowARPL2", 
                                                "id": idNum, 
                                    			"instructions":{
                                    				"instruction": [
                                    					{
                                    						"order":0,
                                    						"apply-actions": {
                                    							"action": [
                                    								{
                                    									"order":0,
                                    									"output-action":{
                                    										"output-node-connector": nodeConnector
                                    									}
                                    								}
                                    							]	
                                    						}
                                    					}
                                    				]
                                    			},
                                                "match": {
                                                    "ethernet-match": {
                                                        "ethernet-destination":{
                                                            "address": macAddress
                                                        }
                                                    }
                                                }, 
                                                "priority": 100, 
                                                "table_id": 30
                                            }
                                        ]
                                    }
                    
                            with open('dataFlowARPL2/dataFlowARPL2'+nodeIDName+'-'+str(x)+'-'+str(address)+'.json','w') as outfile:
                               json.dump(putJson,outfile,sort_keys=True,indent=4)
                            
                            
                            idNum = idNum+1 #after 1 flow is finished for 1 port increase the ID by 1
