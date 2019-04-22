import RestCoAP

testing_flag = 1

class SlotOperation(object):
    def __init__(self, nodeKey, parentID=None ,slot_numbers=None, now_slotoffset=None, now_channeloffset=None):
      self.nodeKey = nodeKey
      self.parentID = parentID
      self.slot_numbers = slot_numbers
      self.now_slotoffset = now_slotoffset
      self.now_channeloffset = now_channeloffset
      self.need_to_added_deled_slot = 0
      self.resource = "slotframe"  # resource name.

      self.child_dict = {}
      
    # for parent node to post other child node.
    def parentPostQuery(self, childID, current_timeslot_offset, current_channel_offset, current_slot_numbers, delFlag):
      childKey = childID.getName()
      slot_offset = child_dict.get(childID)[0]
      channel_offset = child_dict.get(childID)[1]
      slot_numbers = child_dict.get(childID)[2]

      if delFlag is 2:
        if testing_flag :
          print "First Post or Update Parent for new post."

        query = "slot="+str(slot_offset)+"&numbers="+str(slot_numbers)

        RestCoAP.postQueryToNode(childKey, self.resource, query)
        RestCoAP.postQueryToNode(self.nodeKey, self.resource, query) # send by self.

      elif delFlag is 1 :
        print "No changed event."
        pass

      elif delFlag is 0 :
        query = "slot="+str(current_timeslot_offset)+"&numbers="+str(current_slot_numbers)
        delquery = "&delslot="+str(slot_offset)+"&delnumbers="+str(slot_numbers)
        
        query = query + delquery

        child_dict[childID][0] = current_timeslot_offset
        child_dict[childID][1] = current_channel_offset
        child_dict[childID][2] = current_slot_numbers

        # to notification it's parent need add/del new slot.
        self.need_to_added_deled_slot = 1


        if testing_flag :
          print "Got changed event, will be delete slot and then added slot in one step."+" show force query : "+query

        # first delslot, then working will added slot.
        RestCoAP.postQueryToNode(childID.getName(), self.resource, query)
        RestCoAP.postQueryToNode(self.nodeKey, self.resource, query) # send by self.
    
    def delChildKey(self, childKey):
      # child node will call it parent to update child_dict.
      for childid in self.child_dict:
        if cmp(childid.getName(), childKey) is 0:
          if testing_flag :
            print "Deleted child was successful."+str(childid.getName())
          self.child_dict.pop(childid)

    def checkParent(self, parentID):
      # first add child. return 2 to post query.
      if self.parentID is None :
        self.parentID = parentID
        return 2
      else :
        if cmp(parentID.getName(), self.parentID.getName()) is 0:
          if self.need_to_added_deled_slot :
            self.need_to_added_deled_slot = 0 # init
            return 0
          else :
            return 1
        else:
          # callback parentID need to update child_dict.
          self.parentID.delChildKey(self.nodeKey)
          # update parentID
          self.parentID = parentID
          return 0
    
    # if the node is other node's parent, need add to child_dict.
    def checkChild(self, childID, current_slot_offset, current_channel_offset, slot_numbers):
      if childID not in self.child_dict:
        print "add new child : "+childID.getName()+" by "+str(self.nodeKey)
        self.child_dict[childID] = [current_slot_offset, current_channel_offset, slot_numbers]
      
    # get nodeKey name.
    def getName(self):
      return str(self.nodeKey)