import RestCoAP

testing_flag = 1

class SlotOperation(object):
    def __init__(self, nodeKey, parentID=None ,slot_numbers=None, now_slotoffset=None, now_channeloffset=None):
      self.nodeKey = nodeKey
      self.parentID = parentID
      self.slot_numbers = slot_numbers
      self.now_slotoffset = now_slotoffset
      self.now_channeloffset = now_channeloffset
      self.pre_slotoffset = None
      self.pre_channeloffset = None
      self.pre_slot_numbers = None
      self.need_to_added_deled_slot = 0
      self.child_node_of_numbers = None
      self.need_again_add_slot = 0
      self.need_more_slot = 0


      self.child_list = []
      self.old_child_list = []
      self.child_slot_dict = {}
      
    # for parent node to post other child node.
    def parentPostQuery(self, childID, timeslot_offset, channel_offset, resource, query, delFlag):

      
      if delFlag is 2:
        if testing_flag :
          print "First Post or Update Parent for new post."
          print "prev: "+str(self.pre_slotoffset)+", current: "+str(timeslot_offset)+", now: "+str(self.now_slotoffset)

        if childID.checkChile_list :

        # if child was changed, add same as slot to parent.
        if self.need_again_add_slot > 0 :
          query = "slot="+str(timeslot_offset)+"&numbers="+str(need_again_add_slot)
          self.need_more_slot = self.need_again_add_slot
          self.need_again_add_slot = 0

        # update child pre_slot.
        childID.setSlot(timeslot_offset,timeslot_offset)

        # update parent's slot.
        self.updateSlot(timeslot_offset, channel_offset)

        RestCoAP.postQueryToNode(childID.getName(), resource, query)
        RestCoAP.postQueryToNode(self.nodeKey, resource, query) # send by self.

      elif delFlag is 1 :
        print "No changed event."
        pass

      elif delFlag is 0 :
        if self.parentID is None:
          delquery = "&delslot="+str(self.now_slotoffset)+"&delnumbers="+str(self.slot_numbers)
        else :
          delquery = "&delslot="+str(self.pre_slotoffset)+"&delnumbers="+str(self.pre_slot_numbers)
        query = query + delquery

        # to notification it's parent need add/del new slot.
        self.need_to_added_deled_slot = 1

        # update child pre_slot.
        childID.setSlot(timeslot_offset,timeslot_offset)

        if testing_flag :
          print "prev: "+str(self.pre_slotoffset)+", current: "+str(timeslot_offset)+", now: "+str(self.now_slotoffset)
          print "Got changed event, will be delete slot and then added slot in one step."+" show force query : "+query

        # update parent's slot.
        self.updateSlot(timeslot_offset, channel_offset)

        # first delslot, then working will added slot.
        RestCoAP.postQueryToNode(childID.getName(), resource, query)
        RestCoAP.postQueryToNode(self.nodeKey, resource, query) # send by self.
      
    def setSlot(self, timeslot_offset, channel_offset):
      self.pre_slotoffset = timeslot_offset
      self.pre_channeloffset = channel_offset

    def updateSlot(self, timeslot_offset, channel_offset):
      self.pre_slotoffset = self.now_slotoffset # to save 
      self.pre_channeloffset = self.now_channeloffset

      self.now_slotoffset = timeslot_offset # to update offset
      self.now_channeloffset = channel_offset

    def updateSlotNumbers(self, current_slot_numbers):
      self.pre_slot_numbers = self.slot_numbers
      self.slot_numbers = current_slot_numbers
    
    def delChildKey(self, childKey):
      # child node will call it parent to update child_list.
      if len(self.child_list) != 0:
        for childid in self.child_list:
          if cmp(childid.getName(), childKey) is 0:
            if testing_flag :
              print "Deleted child was successful."+str(childid.getName())
            self.child_list.remove(childid)
            self.old_child_list = self.child_list # copy to old_list
            

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
          # callback parentID need to update child_list.
          self.parentID.delChildKey(self.nodeKey)
          # update parentID
          self.parentID = parentID
          return 0
    
    # if the node is other node's parent, need add to child_list.
    def checkChild(self, childID):
      if childID not in self.child_list:
        print "add new child : "+childID.getName()+" by "+str(self.nodeKey)
        self.child_list.append(childID)
        self.child_node_of_numbers = childID.checkChile_list()
      else :
        if self.child_node_of_numbers is not childID.checkChile_list() :
          self.need_again_add_slot = childID.checkChile_list() - self.child_node_of_numbers
          return 1
        elif childID.wasNeedMoreSlot() > 0 :
          self.need_again_add_slot = childID.wasNeedMoreSlot()
          return 1
          
    
    def checkChile_list(self):
      return len(self.child_list)

    def wasNeedMoreSlot(self):
      temp_slot = self.need_more_slot
      self.need_more_slot = 0
      return int(temp_slot)
      
    # get nodeKey name.
    def getName(self):
      return str(self.nodeKey)