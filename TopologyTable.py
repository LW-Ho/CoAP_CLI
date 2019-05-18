import RestCoAP
from SlotOperation import SlotOperation
from NodeLocalQueue import getNodeLocalQueue
from core.nodeinfo import NodeInfo
import core.channelinfo as ChannelInfo

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
nodeDict = None


def set_table(host, topology_List):
  global node_list, g_init_flag
  print node_list
  if len(node_list) == 0 :
    g_init_flag = 1 
  else :
    g_init_flag = 0

  dictTemp = {}

  for item in topology_List:
    #print item
    if item[0] in dictTemp:
      dictTemp[item[0]].append(item[1])
    else:
      dictTemp[item[0]] = [item[1]]

  topology_print(dictTemp, host)

def topology_print(dictTemp, host):
  global global_counter, node_list, node_Name_list, topology_list, nodeDict
  topology_list = []
  get_queue = 0
  hostNode = None
  global_counter = 0 # initialize
  for mainKey in dictTemp.keys():
    if mainKey in host:
      print mainKey # host
      topology_list += [mainKey]
      border_router_ID = mainKey

      if len(node_list) is 0:
        hostNode = SlotOperation(nodeKey=mainKey)
        node_list.append(hostNode)
        node_Name_list.append(hostNode.getName())
        ChannelInfo.initial_channel_list(True)
      else :
        for hostID in node_list:
          if cmp(hostID.getName(), mainKey) is 0 :
            hostNode = hostID
      if nodeDict is None:
        nodeDict = NodeInfo()

      print nodeDict.getNodeTable()
      print node_Name_list
        
      global_counter += 1
      for childKey in dictTemp.get(mainKey):

        # host's child is other node's parent.
        if childKey in dictTemp.keys():

          print "--"+" 1 "+childKey
          topology_list += ["--"+" 1 "+childKey]

          get_queue = parentAndChild(childKey, dictTemp, 1)
 
          temp_local_queue = 1
          if g_init_flag :
            temp_local_queue = getNodeLocalQueue(childKey)
            nodeDict.setNodeInfo(childKey, mainKey, temp_local_queue, get_queue+temp_local_queue)
          else :
            temp_local_queue = nodeDict.getNodeLQ(childKey)

          print nodeDict.getNodeTable()
          
          global_counter += temp_local_queue
          sumCounter = get_queue+temp_local_queue

          # if g_init_flag is 0 :
          #   childparentControl(mainKey, childKey, sumCounter)

          dictTemp.pop(childKey)
 
        # only child
        else: 
          
          temp_local_queue = 1
          if g_init_flag :
            temp_local_queue = getNodeLocalQueue(childKey)
            nodeDict.setNodeInfo(childKey, mainKey, temp_local_queue, temp_local_queue) # save the local queue and global queue.
          else :
            temp_local_queue = nodeDict.getNodeLQ(childKey)

          global_counter += temp_local_queue
        
          # if g_init_flag is 0 :
          #   childparentControl(mainKey, childKey, temp_local_queue)

          print "--"+" 1 "+childKey
          topology_list += ["--"+" 1 "+childKey]

  print ""
  print '\n'.join(topology_list)
  print ""

  # post scheduling to all nodes.
  postSchedulingTable()

  return node_list


def parentAndChild(parentKey, dictTemp, temp_counter):
  global global_counter, slot_offset, node_list, channel_offset, topology_list, nodeDict
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

      temp_local_queue = 1
      if g_init_flag :
        temp_local_queue = getNodeLocalQueue(childKey)
        nodeDict.setNodeInfo(childKey, parentKey, temp_local_queue, get_queue+temp_local_queue)
      else :
        temp_local_queue = nodeDict.getNodeLQ(childKey)

      global_counter += temp_local_queue
      sumCounter = get_queue+temp_local_queue

      local_queue = local_queue + sumCounter # return upper layer.

      # if g_init_flag is 0 :
      #   childparentControl(parentKey, childKey, sumCounter)

      temp_str = ""
      for index in range(0,temp_counter):
        temp_str = temp_str+"--"
      print temp_str+" "+str(temp_counter)+" "+childKey
      topology_list += [temp_str+" "+str(temp_counter)+" "+childKey]

    # end of child.
    else :

      temp_local_queue = 1
      if g_init_flag :
        temp_local_queue = getNodeLocalQueue(childKey)
        nodeDict.setNodeInfo(childKey, parentKey,temp_local_queue, temp_local_queue)
      else :
        temp_local_queue = nodeDict.getNodeLQ(childKey)

      local_queue = local_queue + temp_local_queue # to save it.
      global_counter += temp_local_queue

      # if g_init_flag is 0 :
      #   childparentControl(parentKey, childKey, temp_local_queue)

      temp_str = ""
      for index in range(0,temp_counter+1):
        temp_str = temp_str+"--"
      print temp_str+" "+str(temp_counter+1)+" "+childKey
      topology_list += [temp_str+" "+str(temp_counter+1)+" "+childKey]

  return local_queue

def postSchedulingTable():
  scheDict = nodeDict.getNodeTable()
  maxKey = None

  while (len(scheDict) > 0) :
    scheList = sorted(scheDict.items(), lambda x, y: cmp(x[1][2], y[1][2]), reverse=True)
    for i, v in enumerate(scheList):
      if maxKey is None:
        maxKey = v[0]

      if scheDict.has_key(v[0]) and maxKey == v[0]:
        if v[1][1] != 0 :
          lq = v[1][1]-1
          gq = v[1][2]-1
          scheDict[v[0]] = [v[1][0] , lq, gq]
        if scheDict.has_key(v[1][0]) and v[1][0] != "1" :
          temp = scheDict.get(v[1][0])
          scheDict[v[1][0]] = [temp[0], temp[1]+1, temp[2]]

        childparentControl(v[1][0], v[0], 1)
        print v[0]+" post to "+v[1][0]+", "+str(scheDict[v[0]])

        if lq == 0 and gq == 0:
          print "delete "+v[0]
          scheDict.pop(v[0])
          maxKey = None
          break

      elif maxKey is v[1][0]:

        if v[1][1] != 0 :
            lq = v[1][1]-1
            gq = v[1][2]-1
            scheDict[v[0]] = [v[1][0] , lq, gq]
        if scheDict.has_key(v[1][0]) and v[1][0] != "1" :
          temp = scheDict.get(v[1][0])
          scheDict[v[1][0]] = [temp[0], temp[1]+1, temp[2]]
        
        childparentControl(v[1][0], v[0], 1)
        print v[0]+" post to "+v[1][0]+", *"+str(scheDict[v[0]])
        maxGlobalQueue = 1
          
        if lq == 0 and gq == 0:
          print "delete "+v[0]
          scheDict.pop(v[0])

  


def childparentControl(parentKey, childKey, slot_of_numbers):
  global node_list, node_Name_list
  parentNode = None
  childNode = None

  if parentKey not in node_Name_list :
    if testing_flag :
      print "append "+parentKey+" into node_list"
    parentNode = SlotOperation(nodeKey=parentKey)
    node_list.append(parentNode)
    node_Name_list.append(parentNode.getName())
  else :
    for parentid in node_list :
      # got already exists the parentID
      if cmp(parentKey,parentid.getName()) is 0 :
        parentNode = parentid
  
  if childKey not in node_Name_list :
    if testing_flag :
      print "append "+childKey+" into node_list"
    childNode = SlotOperation(nodeKey=childKey)
    node_list.append(childNode)
    node_Name_list.append(childNode.getName())
  else :
    for nodeid in node_list :
      if cmp(childKey, nodeid.getName()) is 0 :
        childNode = nodeid

  parentFlag_control(parentNode, childNode, slot_of_numbers)
  # return parentNode, childNode

def parentFlag_control(ParentNode, ChildNode, slot_of_numbers):
  # get parent flag event.
  parent_Flag = ChildNode.checkParent(ParentNode)
  # add a child for it's parent node_list.
  topology_Flag = ParentNode.checkChild(ChildNode)
  print topology_Flag
  
  if parent_Flag is 0 :
    # need to delete other parent dedicated slot.
    while slot_of_numbers > 0 :
      slot_offset, channel_offset = ChannelInfo.set_channel_list(ChildNode.getName(), ParentNode.getName(), slot_of_numbers)
      ParentNode.parentPostQuery(ChildNode.getName(), slot_offset, channel_offset, parent_Flag)
      slot_of_numbers = slot_of_numbers - 1
    return 0
  elif parent_Flag is 1 :
    if topology_Flag is 1 :
      return 0
    else :
      while slot_of_numbers > 0 :
        slot_offset, channel_offset = ChannelInfo.set_channel_list(ChildNode.getName(), ParentNode.getName(), slot_of_numbers)
        ParentNode.parentPostQuery(ChildNode.getName(), slot_offset, channel_offset, 0)
        slot_of_numbers = slot_of_numbers - 1
      return 1
    pass
  elif parent_Flag is 2 :
    while slot_of_numbers > 0 :
      slot_offset, channel_offset = ChannelInfo.set_channel_list(ChildNode.getName(), ParentNode.getName(), slot_of_numbers)
      ParentNode.parentPostQuery(ChildNode.getName(), slot_offset, channel_offset, parent_Flag)
      slot_of_numbers = slot_of_numbers - 1
    return 0



def cal_timeslot(now_time_slot, numbers):
  max_numbers = 151
  now_time_slot_offset = now_time_slot + numbers

  if now_time_slot_offset > max_numbers :
    return 1
  else :
    return 0
