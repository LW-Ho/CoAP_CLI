import RestCoAP

class SlotOperation(object):
    def __init__(self, nodeKey, parentID=None ,slot_numbers=None, now_slotoffset=None, now_channeloffset=None):
      self.nodeKey = nodeKey
      self.parentID = parentID
      self.slot_numbers = slot_numbers
      self.now_slotoffset = now_slotoffset
      self.now_channeloffset = now_channeloffset
      self.pre_slotoffset = None
      self.pre_channeloffset = None

      self.child_list = []
      self.child_slot_dict = {}
      
    # for parent node to post other child node.
    def parentPostQuery(self, childID, timeslot_offset, channel_offset, resource, query, delFlag):

      
      if delFlag is 2:
        print "First Post or Update Parent for new post."
        self.pre_slotoffset = timeslot_offset # to save 
        self.pre_channeloffset = channel_offset

        RestCoAP.postQueryToNode(childID.getName(), resource, query)
        RestCoAP.postQueryToNode(self.nodeKey, resource, query) # send by self.
      elif delFlag is 1 :
        print "No changed event."
        pass

      elif delFlag is 0 :
        delquery = "delslot="+str(self.pre_slotoffset)
        query = query + delquery

        print "Got changed event, will be delete slot and then added slot in one step."+" show force query : "+query

        self.pre_slotoffset = timeslot_offset # to update value
        self.pre_channeloffset = channel_offset

        # first delslot, then working will added slot.
        RestCoAP.postQueryToNode(childID.getName(), resource, query)
        RestCoAP.postQueryToNode(self.nodeKey, resource, query) # send by self.

    
    def delChildKey(self, childKey):
      # child node will call it parent to update child_list.
      if len(self.child_list) != 0:
        for childID in self.child_list:
          if cmp(childID.getName(), childKey) is 0:

            self.child_list.remove(childID)
            #print "deleted child was successful."

    def checkParent(self, parentID):

      # first add child. return 2 to post query.
      if self.parentID is None :
        self.parentID = parentID
        return 2
      else :
        if cmp(parentID.getName(), self.parentID.getName()) is 0:
          return 1
        else:
          # callback parentID need to update child_list.
          self.parentID.delChildKey(self.nodeKey)
          # update parentID
          self.parentID = parentID
          return 0
    
    # if the node is other node's parent, need add to child_list.
    def checkChild(self, childID):
      if len(self.child_list) != 0:
        if childID.getName() not in self.child_list:
          self.child_list.append(childID)
          print "add new child : "+childID.getName()+" by "+str(self.nodeKey)
      else:
        self.child_list.append(childID)
      
    # get nodeKey name.
    def getName(self):
      return str(self.nodeKey)