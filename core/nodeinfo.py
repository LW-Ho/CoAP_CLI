class NodeInfo(object):
  def __init__(self):
    self.node_dict = {}

  # save node localqueue
  def setNodeInfo(nodeKey, parentKey, localQueue, globalQueue):
    if nodeKey not in self.node_dict.keys():
      self.node_dict[nodeKey] = [parentKey, int(localQueue), int(globalQueue)]

  def setNodeTable(nodeDict):
    
    self.node_dict = nodeDict
    
  def updateNodeParent(nodeKey, parentKey):
    
    self.node_dict[nodeKey][0] = parentKey

  def updateNodeLQ(nodeKey, localQueue):
    
    self.node_dict[nodeKey][1] = int(localQueue)

  # return node's parentKey
  def getNodeParent(nodeKey):
    
    if nodeKey in self.node_dict.keys():
      # return parentKey by nodeKey.
      return self.node_dict[nodeKey][0]
    else :
      # default
      return None

  # return node local queue
  def getNodeLQ(nodeKey):
    
    print self.node_dict
    if nodeKey in self.node_dict.keys():
      # return localqueue by nodeKey.
      return self.node_dict[nodeKey][1]
    else :
      # default one value.
      return None

  def getNodeQU(nodeKey):
    
    if nodeKey in self.node_dict.keys():
      # return globalqueue by nodeKey.
      return self.node_dict[nodeKey][2]
    else :
      # need to get the global queue of numbers.
      return None

  def getNodeTable():
    
    temp = self.node_dict
    return temp