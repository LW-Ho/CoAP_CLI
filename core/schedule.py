import core.nodeinfo as NodeInfo
import TopologyTable as TopologyTable

handup_list = []
scheDict = {}

def StartSchedule(temp_scheDict):
  global scheDict, handup_list

  scheDict = temp_scheDict
  
  # print scheList
  while (len(scheDict) > 0):
    scheList = sorted(scheDict.items(), lambda x, y: cmp(x[1][2], y[1][2]), reverse=True)
    # to copy the list length, can research the global queue and localqueue
    scheList_length = len(scheList)
    #print scheList
    # init_global_var():

    for i in range(scheList_length) :

      temp = scheList[i]
      temp_NodeKey = temp[0]
      temp_ParentKey = temp[1][0]
      temp_GQueue = temp[1][2]   # global queue
      temp_LQueue = temp[1][1]   # local queue
      # print temp_NodeKey
      # return True/False
      if search_maxQueue(temp_LQueue, temp_GQueue, temp_NodeKey, temp_ParentKey) :
        #compare_queue()
        continue
      else:
        #print "Compare "+temp_NodeKey, scheList[-1][0]
        if temp_NodeKey is scheList[-1][0] :
          # compare which have more queue
          # print "goto compare"
          compare_queue()
          
          break
        else :
          #time.sleep(0.2)
          continue


def search_maxQueue(LQueue, GQueue, NodeKey, ParentKey) :
  # Check if the node still has a packet.
  if LQueue > 0: 
    if len(handup_list) != 0:
      #print NodeKey
      if NodeKey not in handup_list :
        for i in range(len(handup_list)):
          tempNodeKey = handup_list[i]
          #print "1 "+NodeKey+"  "+ParentKey
          tempParentKey = scheDict[tempNodeKey][0]
          #print handup_list
          #print "2 "+tempNodeKey+"  "+tempParentKey
          if NodeKey not in handup_list and ParentKey not in handup_list :
            if ParentKey is not tempNodeKey and ParentKey is not tempParentKey :
              # differnt parent will not happend Half-Duplex collision, can save it.
              #print i+1, len(handup_list)
              if i+1 == len(handup_list) :
                # print "Got the Node : "+NodeKey
                handup_list.append(NodeKey)
                return True
            else :
              return False
          else :
            return False
      else :
        return False

    else :
      # first NodeKey to save in list.
      # print "** Got the Node : "+NodeKey
      handup_list.append(NodeKey)
      return True
  else :
    return False


# return max Global Queue from ParentNode
def calculate_parent_GQ(NodeKey):
  parentKey = scheDict[NodeKey][0]
  if parentKey != "fd00::1" :
    return calculate_parent_GQ(parentKey)
  else :
    return int(scheDict[NodeKey][2])
        
# check which parent queue is larger.
def check_parent_GQ(NodeKey, nextNodeKey):
  if calculate_parent_GQ(NodeKey) > calculate_parent_GQ(nextNodeKey) :
    return True
  elif calculate_parent_GQ(NodeKey) == calculate_parent_GQ(nextNodeKey) :
    return True
  elif calculate_parent_GQ(NodeKey) < calculate_parent_GQ(nextNodeKey) :
    return False
  else :
    return False

# Check the node who have more queue, then pass the packet to next node.
def compare_queue():

  while len(handup_list) > 0 :
    list_length = len(handup_list)
    for i in range(list_length) :
      tempNodeKey = handup_list[i]
      # check parent's global queue
      if scheDict[tempNodeKey][0] != "fd00::1" :
        if list_length > 1:
          if scheDict[tempNodeKey][2] == scheDict[handup_list[i+1]][2] :
            print tempNodeKey, handup_list[i+1]
            if check_parent_GQ(tempNodeKey, handup_list[i+1]) :
              pass_query(tempNodeKey)
            else :
              pass_query(handup_list[i+1])
            break
          else :
            pass_query(tempNodeKey)
            break
        else :
          pass_query(tempNodeKey)
          break
      else :
        pass_query(tempNodeKey)
        break

def pass_query(NodeKey):
  ParentKey = scheDict[NodeKey][0]
  send_count = 0
  if ParentKey != "fd00::1" :
    # other Layer, not first
    # update_NodeInfo(NodeKey, "-")
    send_count = update_NodeInfo(NodeKey, "-")
    update_NodeInfo(ParentKey, "+")
  else :
    # First Layer
    # update_NodeInfo(NodeKey, "-")
    send_count = update_NodeInfo(NodeKey, "-")

  # Post Query To Node
  # Post(NodeKey, ParentKey, send_count)
  if send_count != 0 :
    TopologyTable.slotPostControl(ParentKey, NodeKey, send_count)
  else :
    print "Error from pass_query"

  # --- #
  handup_list.remove(NodeKey)


def update_NodeInfo(NodeKey, operate_flag):
  # print NodeKey
  NodeKey_data = scheDict[NodeKey]
  P_LQ = NodeKey_data[1]
  P_GQ = NodeKey_data[2]
  send_count = NodeKey_data[3]
  if operate_flag is "+" :
    P_LQ += 1
    scheDict[NodeKey] = [NodeKey_data[0], P_LQ, P_GQ, send_count]
  elif operate_flag is "-" :
    P_LQ -= 1
    send_count += 1
    scheDict[NodeKey] = [NodeKey_data[0], P_LQ, P_GQ, send_count]

    print NodeKey+" Post to "+str(NodeKey_data[0])
    
    if P_LQ == 0 and send_count == P_GQ:
      # pop the node.
      # print "Delete "+NodeKey, 
      # print scheDict[NodeKey]
      scheDict.pop(NodeKey)
      
    return send_count