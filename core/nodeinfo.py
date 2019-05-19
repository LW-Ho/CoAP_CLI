
node_dict = {}
mainKey = None
def setMainKey(main_Key):
  global mainKey
  mainKey = main_Key

def getMainKey():
  return mainKey

# save node localqueue
def setNodeInfo(nodeKey, parentKey, localQueue, globalQueue):
  #if nodeKey not in node_dict.keys():
  node_dict[nodeKey] = [parentKey, int(localQueue), int(globalQueue), 0]

def updateNodeParent(nodeKey, parentKey):
  
  node_dict[nodeKey][0] = parentKey

def updateNodeLQ(nodeKey, localQueue):
  
  node_dict[nodeKey][1] = int(localQueue)

def updateNodeGQ(nodeKey, parentKey, localQueue):
  # use recurse loop to update global queue for each parent node.
  while (parentKey != mainKey) :
    node_dict[parentKey][2] += localQueue
    parentKey = node_dict[parentKey][0]

# return node's parentKey
def getNodeParent(nodeKey):
  if nodeKey in node_dict.keys():
    # return parentKey by nodeKey.
    return node_dict[nodeKey][0]
  else :
    # default
    return None

# return node local queue
def getNodeLQ(nodeKey):
  
  if nodeKey in node_dict.keys():
    # return localqueue by nodeKey.
    return node_dict[nodeKey][1]
  else :
    # default one value.
    return None

def getNodeQU(nodeKey):
  if nodeKey in node_dict.keys():
    # return globalqueue by nodeKey.
    return node_dict[nodeKey][2]
  else :
    # need to get the global queue of numbers.
    return None

def getNodeTable():
  return node_dict.copy()