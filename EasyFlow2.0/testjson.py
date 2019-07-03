# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 01:42:38 2019

@author: User
"""
import json

data = {
  "topology": [
    {
      "topology-id": "ovsdb:1",
      "node": [
        {
          "node-id": "ovsdb://HOST1",
          "ovsdb:openvswitch-external-ids": [
            {
              "external-id-key": "opendaylight-iid",
              "external-id-value": "/network-topology:network-topology/network-topology:topology[network-topology:topology-id='ovsdb:1']/network-topology:node[network-topology:node-id='ovsdb://HOST1']"
            }
          ],
          "ovsdb:connection-info": {
            "local-ip": "<controller-ip>",
            "remote-port": 6640,
            "remote-ip": "<ovs-host-ip>",
            "local-port": 39042
          },
          "ovsdb:ovs-version": "2.3.1-git4750c96",
          "ovsdb:manager-entry": [
            {
              "target": "ptcp:6640",
              "connected": True,
              "number_of_connections": 1
            }
          ]
        }
      ]
    }
  ]
}
for person in data['topology']:
    if 'node' not in person:
        print("error")
    else:
        print("me")
if data['topology'] != '':
    print('ye')
        
        