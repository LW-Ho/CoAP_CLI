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
      slot_offset = self.child_dict.get(childID)[0]
      channel_offset = self.child_dict.get(childID)[1]
      slot_numbers = self.child_dict.get(childID)[2]

      # TX = 1 / RX = 2

      if delFlag is 2:
        if testing_flag :
          print "First Post or Update Parent for new post."

        query1 = "slot="+str(slot_offset)+"&numbers="+str(slot_numbers)+"&link=1"
        RestCoAP.postQueryToNode(childKey, self.resource, query1)
        query2 = "slot="+str(slot_offset)+"&numbers="+str(slot_numbers)+"&link=2"
        RestCoAP.postQueryToNode(self.nodeKey, self.resource, query2) # send by self.

      elif delFlag is 1 :
        print "No changed event."
        pass

      elif delFlag is 0 :
        self.child_dict[childID][0] = current_timeslot_offset
        self.child_dict[childID][1] = current_channel_offset
        self.child_dict[childID][2] = current_slot_numbers


        if current_timeslot_offset is 0 and current_channel_offset is 0 and current_slot_numbers is 0 :
          query = "delslot="+str(slot_offset)+"&delnumbers="+str(slot_numbers)
          self.need_to_added_deled_slot = 1

          # first delslot, then working will added slot.
          RestCoAP.postQueryToNode(childID.getName(), self.resource, query)
          RestCoAP.postQueryToNode(self.nodeKey, self.resource, query) # send by self.
        else :
          self.need_to_added_deled_slot = 1

          query1 = "slot="+str(current_timeslot_offset)+"&numbers="+str(current_slot_numbers)+"&link=1"
          delquery1 = "&delslot="+str(slot_offset)+"&delnumbers="+str(slot_numbers)
          query1 = query1 + delquery1
          # first delslot, then working will added slot.
          RestCoAP.postQueryToNode(childID.getName(), self.resource, query1)

          query2 = "slot="+str(current_timeslot_offset)+"&numbers="+str(current_slot_numbers)+"&link=2"
          query2 = query2 + delquery1
          RestCoAP.postQueryToNode(self.nodeKey, self.resource, query2) # send by self.

        if testing_flag :
          print "Got changed event, will be delete slot and then added slot in one step."+" show force query : "+query

    
    def delChildKey(self, childKey):
      # child node will call it parent to update child_dict.
      for childid in self.child_dict.keys():
        if cmp(childid.getName(), childKey) is 0:
          if testing_flag :
            print "Deleted child was successful."+str(childid.getName())+" by "+str(self.nodeKey)
          self.parentPostQuery(childid, 0, 0, 0, 0)
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
        self.child_dict[childID] = [current_slot_offset, current_channel_offset, slot_numbers, childID.getChild_numbers()]

        if testing_flag :
          print "childID get Child Numbers : "+str(childID.getChild_numbers())+" and old child numbers : "+str(self.child_dict[childID][3])

      else :
        if cmp(type(childID.getChild_numbers()), type(self.child_dict[childID][3])) is 0: # match same as type is int.
          if cmp(int(childID.getChild_numbers()),int(self.child_dict[childID][3])) is 1: # not match
            if testing_flag :
              print "childID get Child Numbers : "+str(childID.getChild_numbers())+" and old child numbers : "+str(self.child_dict[childID][3])
            self.child_dict[childID][3] = int(childID.getChild_numbers())
            self.parentPostQuery(childID, current_slot_offset, current_channel_offset, slot_numbers, 0)
            return 1

    def getChild_numbers(self):
      return len(self.child_dict)

    # get nodeKey name.
    def getName(self):
      return str(self.nodeKey)