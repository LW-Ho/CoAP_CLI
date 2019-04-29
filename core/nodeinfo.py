node_dict = {}

# save node localqueue
def saveNodeLQ(nodeKey, localQueue):
  global node_dict
  if nodeKey not in node_dict.keys():
    # first save.
    node_dict[nodeKey] = [int(localQueue)]
  else :
    # update local queue
    node_dict[nodeKey] = [int(localQueue)]

# return node local queue
def getNodeLQ(nodeKey):
  global node_dict
  if nodeKey in node_dict.keys():
    # return localqueue by nodeKey.
    return node_dict[nodeKey][0] 
  else :
    # default one value.
    return 1 