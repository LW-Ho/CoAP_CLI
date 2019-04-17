import RestCoAP

class SlotOperation(object):
    def __init__(self, nodeID, slot_numbers=None, child_numbers=None, now_slotoffset=None, now_channeloffset=None):
      self.nodeID = nodeID
      self.slot_numbers = slot_numbers
      self.is_parent = is_parent
      self.child_numbers = child_numbers
      self.now_slotoffset = now_slotoffset
      self.now_channeloffset = now_channeloffset
      self.pre_slotoffset = None
      self.pre_channeloffset = None

      self.child_list = []

    # for parent node to post other child node.
    def parentpostQuery(self, childID, timeslot_offset, channel_offset, resource, query):
      self.pre_slotoffset = timeslot_offset # to save 
      self.pre_channeloffset = channel_offset

      RestCoAP.postQueryToNode(childID, resource, query)
      RestCoAP.postQueryToNode(self.nodeID, resource, query)

    # if the node is other node's parent, need add to child_list.
    def checkChild(self, childID):
      if len(self.child_list) != 0:
        if childID not in self.child_list:
          self.child_list.append(childID)
      else:
        self.child_list.append(childID)

      return 1
      
    # get nodeID name.
    def getName(self):
      return self.nodeID