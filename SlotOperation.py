import RestCoAP

class SlotOperation(object):
    def __init__(self, nodeID, parentID=None ,slot_numbers=None, now_slotoffset=None, now_channeloffset=None):
      self.nodeID = nodeID
      self.parentID = parentID
      self.slot_numbers = slot_numbers
      self.now_slotoffset = now_slotoffset
      self.now_channeloffset = now_channeloffset
      self.pre_slotoffset = None
      self.pre_channeloffset = None

      self.child_list = []
      
    # for parent node to post other child node.
    def parentpostQuery(self, childID, timeslot_offset, channel_offset, resource, query, delFlag):

      if delFlag is None:
        self.pre_slotoffset = timeslot_offset # to save 
        self.pre_channeloffset = channel_offset

        RestCoAP.postQueryToNode(childID.getName(), resource, query)
        RestCoAP.postQueryToNode(self.nodeID, resource, query) # send by self.

      elif delFlag is 1 :
        delquery = "delslot="+str(self.pre_slotoffset)
        query = query + delquery

        RestCoAP.postQueryToNode(childID.getName(), resource, query)
        RestCoAP.postQueryToNode(self.nodeID, resource, query) # send by self.

        self.pre_slotoffset = timeslot_offset # to update value
        self.pre_channeloffset = channel_offset
    
    def delChildKey(self, childKey):
      # child node will call it parent to update child_list.
      if len(self.child_list) != 0:
        for childID in self.child_list:
          if childID.getName() is childKey:
            self.child_list.remove(childID)
            #print "deleted child was successful."

    def checkParentKey(self, parentKey):
      if parentKey is not self.parentID.getName():
        self.checkParent(self.parentID) # update self parentID
        return 0
      else :
        return 1

    def checkParent(self, parentID):
      if parentID.getName() is self.parentID.getName() :
        return 1
      else:
        # callback parentID need to update child_list.
        self.parentID.delChildKey(self.nodeID)
        # update parentID
        self.parentID = parentID
        return 0
    
    # if the node is other node's parent, need add to child_list.
    def checkChild(self, childID):
      if len(self.child_list) != 0:
        if childID.getName() not in self.child_list:
          if childID.checkParentKey(self.nodeID) is 0 :
            print "child updated parentID"
          self.child_list.append(childID)
          print self.child_list
      else:
        self.child_list.append(childID)
      
    # get nodeID name.
    def getName(self):
      return self.nodeID