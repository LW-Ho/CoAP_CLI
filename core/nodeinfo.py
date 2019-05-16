
node_dict = {}    #to save node information.

# save node localqueue
def setNodeInfo(nodeKey, parentKey, localQueue, globalQueue):
  global node_dict
  if nodeKey not in node_dict.keys():
    node_dict[nodeKey] = [parentKey, int(localQueue), int(globalQueue)]

def setNodeTable(nodeDict):
  global node_dict
  node_dict = nodeDict
  
def updateNodeParent(nodeKey, parentKey):
  global node_dict
  node_dict[nodeKey][0] = parentKey

def updateNodeLQ(nodeKey, localQueue):
  global node_dict
  node_dict[nodeKey][1] = int(localQueue)

# return node's parentKey
def getNodeParent(nodeKey):
  global node_dict
  if nodeKey in node_dict.keys():
    # return parentKey by nodeKey.
    return node_dict[nodeKey][0]
  else :
    # default
    return None

# return node local queue
def getNodeLQ(nodeKey):
  global node_dict
  print node_dict
  if nodeKey in node_dict.keys():
    # return localqueue by nodeKey.
    return node_dict[nodeKey][1]
  else :
    # default one value.
    return None

def getNodeQU(nodeKey):
  global node_dict
  if nodeKey in node_dict.keys():
    # return globalqueue by nodeKey.
    return node_dict[nodeKey][2]
  else :
    # need to get the global queue of numbers.
    return None

def getNodeTable():
  global node_dict
  temp = node_dict
  return temp