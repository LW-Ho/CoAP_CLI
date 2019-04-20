#from core.nodeinfo import NodeInfo
import RestCoAP
from SlotOperation import SlotOperation

node_list = []          # save the node to list. 
node_Name_list = []     # save the node name to list, not class.
global_counter = 0      # save global queue.
testing_flag = 1        # testing flag.
time_slot = 10          # default timeslot_offset.
channel_offset = 0      # default channelslot_offset.
resource = "slotframe"  # resource name.
host_address = ""

def set_table(host, topology_List):
  global node_list

  print node_list
  dictTemp = {}

  for item in topology_List:
    #print item
    if item[0] in dictTemp:
      dictTemp[item[0]].append(item[1])
    else:
      dictTemp[item[0]] = [item[1]]

  topology_print(dictTemp, host)

def topology_print(dictTemp, host):
  global global_counter, time_slot, node_list, channel_offset, node_Name_list, host_address
  local_queue = 1
  get_queue = 0
  hostNode = None
  global_counter = 0 # initialize
  for mainKey in dictTemp.keys():
    if mainKey in host:
      print mainKey # host

      if len(node_list) is 0:
        hostNode = SlotOperation(nodeKey=mainKey)
        node_list.append(hostNode)
        node_Name_list.append(hostNode.getName())
      else :
        for hostID in node_list:
          if cmp(hostID.getName(), mainKey) is 0 :
            hostNode = hostID

      host_address = str(mainKey)
      print node_Name_list
        
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

          nothing_flag = None
          parentNode, childNode = childparentControl(mainKey, childKey, sumCounter)
          nothing_flag = parentFlag_control(parentNode, childNode, time_slot, channel_offset, resource, query)

          if nothing_flag is 0 :
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

          nothing_flag = None
          # only check child
          parentNode, childNode = childparentControl(mainKey, childKey, 1)
          nothing_flag = parentFlag_control(parentNode, childNode, time_slot, channel_offset, resource, query)

          if nothing_flag is 0 :
            time_slot = time_slot + 1

  if testing_flag :
    print "All topology global queue "+str(global_counter)

  return node_list


def parentAndChild(parentKey, dictTemp, temp_counter):
  global global_counter, time_slot, node_list, channel_offset
  local_queue = 0
  get_queue = 0
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
      if cal_timeslot(time_slot, sumCounter) :
        time_slot = 10
      query = "slot="+str(time_slot)+"&numbers="+str(sumCounter)
      
      nothing_flag = None
      parentNode, childNode = childparentControl(parentKey, childKey, sumCounter)
      nothing_flag = parentFlag_control(parentNode, childNode, time_slot, channel_offset, resource, query)

      if nothing_flag is 0 :
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

      nothing_flag = None
      parentNode, childNode = childparentControl(parentKey, childKey, 1)
      nothing_flag = parentFlag_control(parentNode, childNode, time_slot, channel_offset, resource, query)

      if nothing_flag is 0 :
        time_slot = time_slot + 1

  return local_queue

def childparentControl(parentKey, childKey, slot_of_numbers):
  global node_list, node_Name_list, host_address
  parentNode = None
  childNode = None

  if parentKey not in node_Name_list :
    if testing_flag :
      print "append "+parentKey+" into node_list"
    parentNode = SlotOperation(nodeKey=parentKey, slot_numbers=slot_of_numbers, now_slotoffset=time_slot, now_channeloffset=channel_offset)
    node_list.append(parentNode)
    node_Name_list.append(parentNode.getName())
  else :
    for parentid in node_list :
      # got already exists the parentID
      if cmp(parentKey,parentid.getName()) is 0 :
        parentNode = parentid
        parentNode.updateSlotNumbers(slot_of_numbers)
  
  if childKey not in node_Name_list :
    if testing_flag :
      print "append "+childKey+" into node_list"
    childNode = SlotOperation(nodeKey=childKey, slot_numbers=slot_of_numbers, now_slotoffset=time_slot, now_channeloffset=channel_offset)
    node_list.append(childNode)
    node_Name_list.append(childNode.getName())
  else :
    for nodeid in node_list :
      if cmp(childKey, nodeid.getName()) is 0 :
        childNode = nodeid

  return parentNode, childNode

def parentFlag_control(ParentNode, ChildNode, current_timeslot, current_channel_offset, resource, query):
  # get parent flag event.
  parent_Flag = ChildNode.checkParent(ParentNode)
  # add a child for it's parent node_list.
  ParentNode.checkChild(ChildNode)

  if parent_Flag is 0 :
    # need to delete other parent dedicated slot.
    ParentNode.parentPostQuery(ChildNode, current_timeslot, current_channel_offset, resource, query, parent_Flag)
    return 0
  elif parent_Flag is 1 :
    #nothing
    return 1
    pass
  elif parent_Flag is 2 :
    ParentNode.parentPostQuery(ChildNode, current_timeslot, current_channel_offset, resource, query, parent_Flag)
    return 0



def cal_timeslot(now_time_slot, numbers):
  max_numbers = 151
  now_time_slot = now_time_slot + numbers

  if now_time_slot > max_numbers :
    return 1
  else :
    return 0
