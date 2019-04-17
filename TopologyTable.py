#from core.nodeinfo import NodeInfo
import RestCoAP
from SlotOperation import SlotOperation

node_list = []
global_counter = 0
testing_flag = 0
time_slot = 10
channel_offset = 0
resource = "slotframe"

childNode = None
hostNode = None

def cal_timeslot(now_time_slot, numbers):
  max_numbers = 151
  now_time_slot = now_time_slot + numbers

  if now_time_slot > max_numbers :
    now_time_slot = 10
    now_time_slot = now_time_slot + numbers
  
  return now_time_slot

def set_table(host, topology_List):
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
  global childNode, hostNode
  local_queue = 1
  get_queue = 0
  for mainKey in dictTemp.keys():
    if mainKey in host:
      print mainKey # host

      # if host node not in list, add new one.
      if hostNode not in node_list:
        hostNode = SlotOperation(nodeID=mainKey)
        node_list.append(hostNode)

      global_counter += 1
      for childKey in dictTemp.get(mainKey):

        # host's child is other node's parent.
        if childKey in dictTemp.keys(): 
          global_counter += 1
          print "--"+" 1 "+childKey
          get_queue = parentAndChild(childKey, dictTemp, 1)
          
          
          sumCounter = get_queue+local_queue
          time_slot = cal_timeslot(time_slot, sumCounter)
          query = "slot="+str(time_slot)+"&numbers="+str(sumCounter)
          RestCoAP.postQueryToNode(childKey, resource, query)
          RestCoAP.postQueryToNode(mainKey, resource, query)
          
          #time_slot = time_slot + sumCounter

          dictTemp.pop(childKey)
          if testing_flag :
            print childKey+" global queue "+str(get_queue+local_queue)
        # only child
        else: 
          global_counter += 1
          print "--"+" 1 "+childKey
          time_slot = cal_timeslot(time_slot, 1)
          query = "slot="+str(time_slot)

          if len(node_list) != 0 :
            for nodeid in node_list :
              # if node still on first layer and no child.
              if nodeid.getName() is not childKey :
                childNode = SlotOperation(nodeID=childKey, slot_numbers=1, now_slotoffset=time_slot, now_channeloffset=channel_offset)
                node_list.append(childNode)

          # add a child for host node.
          hostNode.checkChild(childKey)
          
          # host node can post node and itself.
          hostNode.parentpostQuery(childNode, time_slot, channel_offset, resource ,query)
          # RestCoAP.postQueryToNode(childKey, resource, query)
          # RestCoAP.postQueryToNode(mainKey, resource, query)
          #time_slot = time_slot + 1


  if testing_flag :
    print "All topology global queue "+str(global_counter)


def parentAndChild(parentKey, dictTemp, temp_counter):
  global global_counter, time_slot, node_list
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
      time_slot = cal_timeslot(time_slot, sumCounter)
      query = "slot="+str(time_slot)+"&numbers="+str(sumCounter)
      RestCoAP.postQueryToNode(childKey, resource, query)
      RestCoAP.postQueryToNode(parentKey, resource, query)
      #time_slot = time_slot + sumCounter
      
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
      time_slot = cal_timeslot(time_slot, 1)
      RestCoAP.postQueryToNode(childKey, resource, query)
      RestCoAP.postQueryToNode(parentKey, resource, query)
      #time_slot = time_slot + 1

  return local_queue