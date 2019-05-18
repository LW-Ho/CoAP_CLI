class NodeInfo:
  def __init__(self):
    self.node_dict = {}

  # save node localqueue
  def setNodeInfo(self, nodeKey, parentKey, localQueue, globalQueue):
    if nodeKey not in self.node_dict.keys():
      self.node_dict[nodeKey] = [parentKey, int(localQueue), int(globalQueue)]

  def updateNodeParent(self, nodeKey, parentKey):
    
    self.node_dict[nodeKey][0] = parentKey

  def updateNodeLQ(self, nodeKey, localQueue):
    
    self.node_dict[nodeKey][1] = int(localQueue)

  # return node's parentKey
  def getNodeParent(self, nodeKey):
    
    if nodeKey in self.node_dict.keys():
      # return parentKey by nodeKey.
      return self.node_dict[nodeKey][0]
    else :
      # default
      return None

  # return node local queue
  def getNodeLQ(self, nodeKey):
    
    print self.node_dict
    if nodeKey in self.node_dict.keys():
      # return localqueue by nodeKey.
      return self.node_dict[nodeKey][1]
    else :
      # default one value.
      return None

  def getNodeQU(self, nodeKey):
    
    if nodeKey in self.node_dict.keys():
      # return globalqueue by nodeKey.
      return self.node_dict[nodeKey][2]
    else :
      # need to get the global queue of numbers.
      return None

  def getNodeTable(self):
    
    return self.node_dict.copy()