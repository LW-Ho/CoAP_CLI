#from core.nodeinfo import NodeInfo
import RestCoAP
from SlotOperation import SlotOperation

node_list = []          # save the node to list. 
global_counter = 0      # save global queue.
testing_flag = 0        # testing flag.
time_slot = 10          # default timeslot_offset.
channel_offset = 0      # default channelslot_offset.
resource = "slotframe"  # resource name.

def set_table(host, topology_List, old_node_list):
  global node_list
  node_list = old_node_list
  dictTemp = {}

  for item in topology_List:
    #print item
    if item[0] in dictTemp:
      dictTemp[item[0]].append(item[1])
    else:
      dictTemp[item[0]] = [item[1]]

  topology_print(dictTemp, host)

def topology_print(dictTemp, host):
  global global_counter, time_slot, node_list, channel_offset
  local_queue = 1
  get_queue = 0
  for mainKey in dictTemp.keys():
    if mainKey in host:
      print mainKey # host

      hostNode = None
      # if host node not in list, add new one.
      if hostNode not in node_list:
        hostNode = SlotOperation(nodeID=mainKey)
        node_list.append(hostNode)
      else :
        for hostID in node_list:
          if hostID.getName() is mainKey:
            hostNode = hostID

      global_counter += 1
      for childKey in dictTemp.get(mainKey):

        # host's child is other node's parent.
        if childKey in dictTemp.keys(): 
          global_counter += 1
          print "--"+" 1 "+childKey
          get_queue = parentAndChild(childKey, dictTemp, 1)
          
          
          sumCounter = get_queue+local_queue
          # check timeslot_offset have larger than TSCH_SLOTFRAME_LENGTH
          if cal_timeslot(time_slot, 1) :
            time_slot = 10
          query = "slot="+str(time_slot)+"&numbers="+str(sumCounter)

          parentFlag = None
          if len(node_list) != 0 :
            for nodeid in node_list :
              # if node have not created, just new one.
              if nodeid.getName() is not childKey :
                childNode = SlotOperation(nodeID=childKey, parentID=hostNode, slot_numbers=sumCounter, now_slotoffset=time_slot, now_channeloffset=channel_offset)
                node_list.append(childNode)
                parentFlag = None
                break
              # got already exists the nodeID
              elif nodeid.getName() is childKey:
                # Confirm that his parent is still the same?
                childNode = nodeid
                if childNode.checkParent(hostNode) :
                  # yes, not send slot_operation again.
                  parentFlag = 0
                else :
                  # no, delete previous slot, then send a new scheduling to node.
                  parentFlag = 1

          

          if parentFlag :
            # add a child for host node_list.
            hostNode.checkChild(childNode)
            # need to delete other parent dedicated slot.
            hostNode.parentPostQuery(childNode, time_slot, channel_offset, resource, query, parentFlag)
          elif parentFlag is 0:
            pass
          else :
            hostNode.parentPostQuery(childNode, time_slot, channel_offset, resource, query, None)

          time_slot = time_slot + sumCounter

          dictTemp.pop(childKey)
          if testing_flag :
            print childKey+" global queue "+str(get_queue+local_queue)
        # only child
        else: 
          global_counter += 1
          print "--"+" 1 "+childKey
          # check timeslot_offset have larger than TSCH_SLOTFRAME_LENGTH
          if cal_timeslot(time_slot, 1) :
            time_slot = 10
          query = "slot="+str(time_slot)

          parentFlag = None
          if len(node_list) != 0 :
            for nodeid in node_list :
              # if node still on first layer and no child.
              if nodeid.getName() is not childKey :
                print "Created a new childNode "+str(childKey)+"."
                childNode = SlotOperation(nodeID=childKey, parentID=hostNode, slot_numbers=1, now_slotoffset=time_slot, now_channeloffset=channel_offset)
                node_list.append(childNode)
                parentFlag = None
                break
              elif nodeid.getName() is childKey:
                # Confirm that his parent is still the same?
                childNode = nodeid
                if childNode.checkParent(hostNode) :
                  # yes, not send slot_operation again.
                  parentFlag = 0
                else :
                  # no, delete previous slot, then send a new scheduling to node.
                  parentFlag = 1
                  
          
          if parentFlag :
            # add a child for host node_list.
            hostNode.checkChild(childNode)
            # need to delete other parent dedicated slot.
            hostNode.parentPostQuery(childNode, time_slot, channel_offset, resource, query, parentFlag)
          elif parentFlag is 0:
            pass
          else :
            hostNode.parentPostQuery(childNode, time_slot, channel_offset, resource, query, None)

          time_slot = time_slot + 1


  if testing_flag :
    print "All topology global queue "+str(global_counter)

  return node_list


def parentAndChild(parentKey, dictTemp, temp_counter):
  global global_counter, time_slot, node_list, channel_offset
  local_queue = 0
  get_queue = 0
  parentNode = None
  save_counter = temp_counter
  for childKey in dictTemp.get(parentKey):
    
    # child still is another child's parent.
    if childKey in dictTemp.keys(): 
      global_counter += 1
      
      temp_counter += 1

      temp_str = ""
      for index in range(0,temp_counter):
        temp_str = temp_str+"--"  
      print temp_str+" "+str(temp_counter)+" "+childKey
      get_queue = parentAndChild(childKey, dictTemp, temp_counter)
      # local_queue += 1
      # no other child, restore uplayer of numbers.
      temp_counter = save_counter 
      local_queue += get_queue
      local_queue += 1
      
      sumCounter = get_queue+1
      # check timeslot_offset have larger than TSCH_SLOTFRAME_LENGTH
      if cal_timeslot(time_slot, 1) :
        time_slot = 10
      query = "slot="+str(time_slot)+"&numbers="+str(sumCounter)
      
      parentFlag = None
      if len(node_list) != 0 :
        for parentid in node_list :
          if parentid.getName() is not parentKey:
            parentNode = SlotOperation(nodeID=parentKey, slot_numbers=sumCounter, now_slotoffset=time_slot, now_channeloffset=channel_offset)
            node_list.append(parentNode)
          else :
            parentNode = parentid

        for nodeid in node_list :
          # if node have not created, just new one.
          if nodeid.getName() is not childKey :
            childNode = SlotOperation(nodeID=childKey, parentID=parentNode, slot_numbers=sumCounter, now_slotoffset=time_slot, now_channeloffset=channel_offset)
            node_list.append(childNode)
            parentFlag = None
            break
          # got already exists the nodeID
          elif nodeid.getName() is childKey:
            # Confirm that his parent is still the same?
            childNode = nodeid
            if childNode.checkParent(parentNode) :
              # yes, not send slot_operation again.
              parentFlag = 0
            else :
              # no, delete previous slot, then send a new scheduling to node.
              parentFlag = 1
        
      if parentFlag :
        # add a child for host node_list.
        parentNode.checkChild(childNode)
        # need to delete other parent dedicated slot.
        parentNode.parentPostQuery(childNode, time_slot, channel_offset, resource, query, parentFlag)
      elif parentFlag is 0:
        pass
      else :
        parentNode.parentPostQuery(childNode, time_slot, channel_offset, resource, query, None)

      time_slot = time_slot + sumCounter
      
      if testing_flag :
        print childKey+" global queue "+str(get_queue+1)

    # end of child.
    else :
      global_counter += 1
      local_queue += 1
      temp_str = ""
      for index in range(0,temp_counter+1):
        temp_str = temp_str+"--"
      print temp_str+" "+str(temp_counter+1)+" "+childKey

      query = "slot="+str(time_slot)

      # check timeslot_offset have larger than TSCH_SLOTFRAME_LENGTH
      if cal_timeslot(time_slot, 1) :
        time_slot = 10

      parentFlag = None
      if len(node_list) != 0 :
        for parentid in node_list :
          # the parent node are not created, we create a new one.
          if parentid.getName() is not parentKey:
            parentNode = SlotOperation(nodeID=parentKey, slot_numbers=1, now_slotoffset=time_slot, now_channeloffset=channel_offset)
            node_list.append(parentNode)
          else :
            parentNode = parentid

        for nodeid in node_list :
          # if node still on first layer and no child.
          if nodeid.getName() is not childKey :
            childNode = SlotOperation(nodeID=childKey, parentID=parentNode ,slot_numbers=1, now_slotoffset=time_slot, now_channeloffset=channel_offset)
            node_list.append(childNode)
            parentFlag = None
            break
          # got already exists the nodeID
          elif nodeid.getName() is childKey:
            # Confirm that his parent is still the same?
            childNode = nodeid
            if childNode.checkParent(parentNode) :
              # yes, not send slot_operation again.
              parentFlag = 0
            else :
              # no, delete previous slot, then send a new scheduling to node.
              parentFlag = 1

      if parentFlag :
        # add a child for host node_list.
        parentNode.checkChild(childNode)
        # need to delete other parent dedicated slot.
        parentNode.parentPostQuery(childNode, time_slot, channel_offset, resource, query, parentFlag)
      elif parentFlag is 0:
        pass
      else :
        parentNode.parentPostQuery(childNode, time_slot, channel_offset, resource, query, None)

      time_slot = time_slot + 1

  return local_queue




def cal_timeslot(now_time_slot, numbers):
  max_numbers = 151
  now_time_slot = now_time_slot + numbers

  if now_time_slot > max_numbers :
    return 1
  else :
    return 0
