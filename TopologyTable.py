import RestCoAP
from SlotOperation import PostQuery
from NodeLocalQueue import getNodeLocalQueue
import core.nodeinfo as NodeInfo
import core.channelinfo as ChannelInfo
import operator

node_list = []          # save the node to list. 
node_Name_list = []     # save the node name to list, not class.
global_counter = 0      # save global queue.
testing_flag = 0        # testing flag.
# slot_offset = 10          # default timeslot_offset.
# channel_offset = 0      # default channelslot_offset.
channel_offset_numbers = 16 # the number is channel offset of total numbers.
g_init_flag = None      # to get node local queue on first search.
topology_list = []
border_router_ID = None
temp_list = []


def set_table(host, topology_List):
  global node_list, g_init_flag
  # print node_list
  # if len(node_list) == 0 :
  #   g_init_flag = 1 
  # else :
  #   g_init_flag = 0

  dictTemp = {}

  for item in topology_List:
    #print item
    if item[0] in dictTemp:
      dictTemp[item[0]].append(item[1])
    else:
      dictTemp[item[0]] = [item[1]]

  topology_print(dictTemp, host)

def topology_print(dictTemp, host):
  global global_counter, node_list, node_Name_list, topology_list, temp_list
  topology_list = []
  get_queue = 0

  global_counter = 0 # initialize
  for mainKey in dictTemp.keys():
    if mainKey in host:
      print mainKey # host
      topology_list += [mainKey]
      border_router_ID = mainKey

      if len(temp_list) is 0:
        #hostNode = SlotOperation(nodeKey=mainKey)
        # node_list.append(hostNode)
        #node_Name_list.append(hostNode.getName())
        ChannelInfo.initial_channel_list(True)

      NodeInfo.setMainKey(mainKey)
      #print node_Name_list
        
      global_counter += 1
      for childKey in dictTemp.get(mainKey):

        # host's child is other node's parent.
        if childKey in dictTemp.keys():

          topology_list += ["--"+" 1 "+childKey]

          get_queue = parentAndChild(childKey, dictTemp, 1)

          temp_local_queue = NodeInfo.getNodeLQ(childKey)
          if temp_local_queue is None :
            temp_local_queue = getNodeLocalQueue(childKey)
          
          NodeInfo.setNodeInfo(childKey, mainKey, temp_local_queue, get_queue+temp_local_queue)

          
          global_counter += temp_local_queue
          sumCounter = get_queue+temp_local_queue

          dictTemp.pop(childKey)
 
        # only child
        else: 

          temp_local_queue = NodeInfo.getNodeLQ(childKey)
          if temp_local_queue is None:
            temp_local_queue = getNodeLocalQueue(childKey)
          
          NodeInfo.setNodeInfo(childKey, mainKey, temp_local_queue, temp_local_queue) # save the local queue and global queue.
          
          global_counter += temp_local_queue

          topology_list += ["--"+" 1 "+childKey]

  if operator.eq(temp_list, topology_list) : 
    pass
  else :
    temp_list = topology_list
    # post scheduling to all nodes.
    postSchedulingTable()

  print ""
  print '\n'.join(topology_list)
  print ""

  return node_list


def parentAndChild(parentKey, dictTemp, temp_counter):
  global global_counter, slot_offset, node_list, channel_offset, topology_list
  local_queue = 0
  get_queue = 0
  save_counter = temp_counter
  for childKey in dictTemp.get(parentKey):
    
    # child still is another child's parent.
    if childKey in dictTemp.keys(): 
      
      temp_counter += 1

      get_queue = parentAndChild(childKey, dictTemp, temp_counter)
      # no other child, restore uplayer of numbers.
      temp_counter = save_counter 

      temp_local_queue = NodeInfo.getNodeLQ(childKey)

      if temp_local_queue is None:
        temp_local_queue = getNodeLocalQueue(childKey)
      
      NodeInfo.setNodeInfo(childKey, parentKey, temp_local_queue, get_queue+temp_local_queue)

      global_counter += temp_local_queue
      sumCounter = get_queue+temp_local_queue

      local_queue = local_queue + sumCounter # return upper layer.

      temp_str = ""
      for index in range(0,temp_counter):
        temp_str = temp_str+"--"
      topology_list += [temp_str+" "+str(temp_counter)+" "+childKey]

    # end of child.
    else :

      temp_local_queue = NodeInfo.getNodeLQ(childKey)

      if temp_local_queue is None :
        temp_local_queue = getNodeLocalQueue(childKey)
      
      NodeInfo.setNodeInfo(childKey, parentKey,temp_local_queue, temp_local_queue)

      local_queue = local_queue + temp_local_queue # to save it.
      global_counter += temp_local_queue

      temp_str = ""
      for index in range(0,temp_counter+1):
        temp_str = temp_str+"--"
      topology_list += [temp_str+" "+str(temp_counter+1)+" "+childKey]

  return local_queue

def postSchedulingTable():
  scheDict = NodeInfo.getNodeTable()
  maxKey = None

  while (len(scheDict) > 0) :
    scheList = sorted(scheDict.items(), lambda x, y: cmp(x[1][2], y[1][2]), reverse=True)
    # print scheList
    for v in scheList:
      if maxKey is None:
        maxKey = v[0]

      if scheDict.has_key(v[0]) and maxKey == v[0]:
        if v[1][1] != 0 :
          lq = v[1][1]-1
          gq = v[1][2]-1
          send_count = v[1][3]+1
          scheDict[v[0]] = [v[1][0] , lq, gq, send_count]
          if scheDict.has_key(v[1][0]) and v[1][0] != "1" :
            temp = scheDict.get(v[1][0])
            scheDict[v[1][0]] = [temp[0], temp[1]+1, temp[2], temp[3]]

          slotPostControl(v[1][0], v[0], send_count)
          print v[0]+" post to "+v[1][0]+", "+str(scheDict[v[0]])

          if lq == 0 and gq == 0:
            print "delete "+v[0]
            scheDict.pop(v[0])
            maxKey = None
            break
        else :
          break

      elif maxKey == v[1][0]:

        if v[1][1] != 0 :
          lq = v[1][1]-1
          gq = v[1][2]-1
          send_count = v[1][3]+1
          scheDict[v[0]] = [v[1][0] , lq, gq, send_count]
          if scheDict.has_key(v[1][0]) and v[1][0] != "1" :
            temp = scheDict.get(v[1][0])
            scheDict[v[1][0]] = [temp[0], temp[1]+1, temp[2], temp[3]]
          
          slotPostControl(v[1][0], v[0], send_count)
          print v[0]+" post to "+v[1][0]+", *"+str(scheDict[v[0]])
          maxGlobalQueue = 1
            
          if lq == 0 and gq == 0:
            print "delete "+v[0]
            scheDict.pop(v[0])
            break
        else :
          break
      
      # else :
      #   print maxKey
      #   print scheDict
      #   print "oops..."

def slotPostControl(parentKey, childKey, send_count):
  # first need to check the child have been changed parent ?
  parent_flag = 1

  while (parent_flag != 0):
    parent_flag, channel_offset = ChannelInfo.check_parent_changed(childKey, parentKey)

    if parent_flag is 0 :
      slot_offset, channel_offset = ChannelInfo.peek_get_channel_list(childKey, parentKey, send_count)
      if slot_offset == 0 :
        # a new slot setting.
        print "add channel and slot."
        slot_offset, channel_offset = ChannelInfo.set_channel_list(childKey, parentKey, 1)
        PostQuery(childKey, parentKey, slot_offset, channel_offset, 0, 1)

      else :
        # already setting, not chaned.
        if ChannelInfo.peek_set_channel_list(childKey, parentKey, slot_offset, channel_offset, send_count) :
          print "got same slot and channel."
          # nothing
    else :
      print "Hello~"
      # need to edit, trigger topology was changed.
      remove_slot(childKey, parent_flag ,channel_offset)


def remove_slot(childKey, del_slot, del_channel):
  print "remove slot."+childKey+" "+str(del_slot)+" "+str(del_channel)
  old_parentKey = ChannelInfo.remove_channel_list(del_slot, del_channel)
  PostQuery(childKey, old_parentKey, 0, 0, del_slot, 2)

  if cmp(old_parentKey, NodeInfo.getMainKey()) is 0 :
    return 1
  else :
    next_old_parentKey, next_old_slot, next_old_channel = ChannelInfo.peek_next_parent_channel_list(old_parentKey, del_slot, del_channel)
    remove_slot(old_parentKey, next_old_slot, next_old_channel)


      
  


# def childparentControl(parentKey, childKey, slot_of_numbers):
#   global node_list, node_Name_list
#   parentNode = None
#   childNode = None

#   if parentKey not in node_Name_list :
#     if testing_flag :
#       print "append "+parentKey+" into node_list"
#     parentNode = SlotOperation(nodeKey=parentKey)
#     node_list.append(parentNode)
#     node_Name_list.append(parentNode.getName())
#   else :
#     for parentid in node_list :
#       # got already exists the parentID
#       if cmp(parentKey,parentid.getName()) is 0 :
#         parentNode = parentid
  
#   if childKey not in node_Name_list :
#     if testing_flag :
#       print "append "+childKey+" into node_list"
#     childNode = SlotOperation(nodeKey=childKey)
#     node_list.append(childNode)
#     node_Name_list.append(childNode.getName())
#   else :
#     for nodeid in node_list :
#       if cmp(childKey, nodeid.getName()) is 0 :
#         childNode = nodeid

#   parentFlag_control(parentNode, childNode, slot_of_numbers)
#   # return parentNode, childNode

# def parentFlag_control(ParentNode, ChildNode, slot_of_numbers):
#   # get parent flag event.
#   parent_Flag = ChildNode.checkParent(ParentNode)
#   # add a child for it's parent node_list.
#   topology_Flag = ParentNode.checkChild(ChildNode)
#   print topology_Flag
  
#   if parent_Flag is 0 :
#     # need to delete other parent dedicated slot.
#     while slot_of_numbers > 0 :
#       slot_offset, channel_offset = ChannelInfo.set_channel_list(ChildNode.getName(), ParentNode.getName(), slot_of_numbers)
#       ParentNode.parentPostQuery(ChildNode.getName(), slot_offset, channel_offset, parent_Flag)
#       slot_of_numbers = slot_of_numbers - 1
#     return 0
#   elif parent_Flag is 1 :
#     if topology_Flag is 1 :
#       return 0
#     else :
#       if NodeInfo.getNodeQU(ChildNode.getName()) is not ChannelInfo.peek_get_channel_list(ChildNode.getName(), ParentNode.getName()) :
#         while slot_of_numbers > 0 :
#           slot_offset, channel_offset = ChannelInfo.set_channel_list(ChildNode.getName(), ParentNode.getName(), slot_of_numbers)
#           ParentNode.parentPostQuery(ChildNode.getName(), slot_offset, channel_offset, 0)
#           slot_of_numbers = slot_of_numbers - 1
#       return 1
#     pass
#   elif parent_Flag is 2 :
#     while slot_of_numbers > 0 :
#       slot_offset, channel_offset = ChannelInfo.set_channel_list(ChildNode.getName(), ParentNode.getName(), slot_of_numbers)
#       ParentNode.parentPostQuery(ChildNode.getName(), slot_offset, channel_offset, parent_Flag)
#       slot_of_numbers = slot_of_numbers - 1
#     return 0



def cal_timeslot(now_time_slot, numbers):
  max_numbers = 151
  now_time_slot_offset = now_time_slot + numbers

  if now_time_slot_offset > max_numbers :
    return 1
  else :
    return 0
