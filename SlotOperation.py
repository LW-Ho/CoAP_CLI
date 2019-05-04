import RestCoAP
import core.channelinfo as ChannelInfo

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
    def parentPostQuery(self, childKey, current_timeslot_offset, current_channel_offset, delFlag):
      print current_timeslot_offset , current_channel_offset

      # TX = 1 / RX = 2
      if delFlag is 2:
        if testing_flag :
          print "First Post or Update Parent for new post."

        
        query1 = "slot="+str(current_timeslot_offset)+"&chanl="+str(current_channel_offset)+"&numbers="+str(1)+"&link=TX"
        RestCoAP.postQueryToNode(childKey, self.resource, query1)
        query2 = "slot="+str(current_timeslot_offset)+"&chanl="+str(current_channel_offset)+"&numbers="+str(1)+"&link=RX"
        RestCoAP.postQueryToNode(self.nodeKey, self.resource, query2) # send by self.

      elif delFlag is 1 :
        print "No changed event."
        pass

      elif delFlag is 0 :

        self.need_to_added_deled_slot = 1

        query1 = "slot="+str(current_timeslot_offset)+"&chanl="+str(current_channel_offset)+"&numbers="+str(1)+"&link=TX"
        # first delslot, then working will added slot.
        RestCoAP.postQueryToNode(childKey, self.resource, query1)

        query2 = "slot="+str(current_timeslot_offset)+"&chanl="+str(current_channel_offset)+"&numbers="+str(1)+"&link=RX"
        RestCoAP.postQueryToNode(self.nodeKey, self.resource, query2) # send by self.

      elif delFlag is 3 :
        query = "delslot="+str(current_timeslot_offset)+"&delnumbers="+str(1)

        # first delslot, then working will added slot.
        RestCoAP.postQueryToNode(childKey, self.resource, query)
        RestCoAP.postQueryToNode(self.nodeKey, self.resource, query) # send by self.

    def delChildKey_callback(self, childKey):
      if testing_flag :
            print "Deleted child was successful."+str(childKey)+" by "+str(self.nodeKey)
      current_slot_offset, current_channel_offset = ChannelInfo.get_channel_list(childKey, self.nodeKey)
      self.parentPostQuery(childKey, current_slot_offset, current_channel_offset, 3)


    
    def delChildKey(self, childKey):
      # child node will call it parent to update child_dict.
      for childid in self.child_dict.keys():
        if cmp(childid.getName(), childKey) is 0:
          if testing_flag :
            print "Deleted child was successful."+str(childid.getName())+" by "+str(self.nodeKey)
          current_slot_offset = 10
          while current_slot_offset > 0 :
            current_slot_offset, current_channel_offset = ChannelInfo.get_channel_list(childid.getName(), self.nodeKey)
            if current_slot_offset is 0 :
              break
            self.parentPostQuery(childid.getName(), current_slot_offset, current_channel_offset, 3)
            if self.parentID is not None :
              self.parentID.delChildKey_callback(self.nodeKey)

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
    def checkChild(self, childID):
      if childID not in self.child_dict:
        print "add new child : "+childID.getName()+" by "+str(self.nodeKey)
        self.child_dict[childID] = [childID.getChild_numbers()]

        if testing_flag :
          print "childID get Child Numbers : "+str(childID.getChild_numbers())+" and old child numbers : "+str(self.child_dict[childID][0])

      else :
        if cmp(type(childID.getChild_numbers()), type(self.child_dict[childID])) is 0: # match same as type is int.
          if cmp(int(childID.getChild_numbers()),int(self.child_dict[childID])) is 1: # not match
            if testing_flag :
              print "childID get Child Numbers : "+str(childID.getChild_numbers())+" and old child numbers : "+str(self.child_dict[childID][0])
            self.child_dict[childID] = int(childID.getChild_numbers())
            current_slot_offset = 10
            while current_slot_offset > 0 :
              current_slot_offset, current_channel_offset = ChannelInfo.get_channel_list(childID.getName(), self.nodeKey)
              if current_slot_offset is 0 :
                break
              self.parentPostQuery(childID.getName(), current_slot_offset, current_channel_offset, 0)

            return 1

    def getChild_numbers(self):
      return len(self.child_dict)

    # get nodeKey name.
    def getName(self):
      return str(self.nodeKey)