import json
import logging
print = logging.info
from ETS2LA.backend.variables import *
from ETS2LA.backend.settings import *
import sys

class Item:
    Uid = 0
    Type = ""

class Node:
    Uid = 0
    X = 0
    Y = 0
    Z = 0
    rX = 0
    rY = 0
    rZ = 0
    Rotation = 0
    ForwardItem = None
    BackwardItem = None
    
nodes = []
optimizedNodes = {}
nodeFileName = PATH + "ETS2LA/plugins/Map/GameData/nodes.json"

from functools import reduce
from operator import getitem
# https://stackoverflow.com/a/70377616
def set_nested_item(dataDict, mapList, val):
    """Set item in nested dictionary"""
    current_dict = dataDict
    for key in mapList[:-1]:
        current_dict = current_dict.setdefault(key, {})
    current_dict[mapList[-1]] = val
    return dataDict

def get_nested_item(dataDict, mapList):
    """Get item in nested dictionary"""
    for k in mapList:
        dataDict = dataDict[k]
    return dataDict

def LoadNodes():
    global nodes
    global optimizedNodes
    
    jsonData = json.load(open(nodeFileName))
    jsonLength = len(jsonData)
    
    sys.stdout.write(f"\nLoading {jsonLength} nodes...\n")
    
    count = 0
    for node in jsonData:
        nodeObj = Node()
        nodeObj.Uid = node["Uid"]
        nodeObj.X = node["X"]
        nodeObj.Y = node["Y"]
        nodeObj.Z = node["Z"]
        nodeObj.rX = node["rX"]
        nodeObj.rY = node["rY"]
        nodeObj.rZ = node["rZ"]
        nodeObj.Rotation = node["Rotation"]
        try:
            nodeObj.ForwardItem = Item()
            nodeObj.ForwardItem.Uid = node["ForwardItem"]["Uid"]
            nodeObj.ForwardItem.Type = node["ForwardItem"]["Type"]
        except:
            nodeObj.ForwardItem = None
            
        try:
            nodeObj.BackwardItem = Item()
            nodeObj.BackwardItem.Uid = node["BackwardItem"]["Uid"]
            nodeObj.BackwardItem.Type = node["BackwardItem"]["Type"]
        except:
            nodeObj.BackwardItem = None
        
        nodes.append(nodeObj)
        count += 1
        
        if count % int(jsonLength/10) == 0:
            sys.stdout.write(f" > {count} ({round(count/jsonLength*100)}%)...\r")
            
    sys.stdout.write(f" > {count} ({round(count/jsonLength*100)}%)... done!\n")
    
    sys.stdout.write(f" > Optimizing node dictionary...\r")      
    
    for node in nodes:
        # Split the node Uid into parts of 3
        uidParts = [str(node.Uid)[i:i+3] for i in range(0, len(str(node.Uid)), 3)]
        # Build the optimizedNodes dictionary
        set_nested_item(optimizedNodes, uidParts, node)
    
    sys.stdout.write(f" > Optimizing node dictionary... done!\n")
    
    print(f"Node parsing done!")
    
def GetNodeByUid(uid):
    
    if uid == 0:
        return None
    if uid == None:
        return None
    
    uidParts = [str(uid)[i:i+3] for i in range(0, len(str(uid)), 3)]
    try:
        node = get_nested_item(optimizedNodes, uidParts)
        if node != None:
            return node
        sys.stdout.write(f" > Node not found in optimizedNodes, searching in nodes...\n")
        for node in nodes:
            if node.Uid == uid:
                return node
    except:
        sys.stdout.write(f" > Node not found in optimizedNodes, searching in nodes...\n")
        for node in nodes:
            if node.Uid == uid:
                return node
        
    return None