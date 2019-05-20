import core.nodeinfo as NodeInfo
import TopologyTable as TopologyTable

scheList = []
scheDict = {}
maxKey_list = []
lastKey = None

def StartSchedule(sche_dict):
  global scheDict, scheList, maxKey_list, lastKey
  scheDict = sche_dict
  while (len(scheDict) > 0):
    scheList = sorted(scheDict.items(), lambda x, y: cmp(x[1][2], y[1][2]), reverse=True)

    for v in scheList:
      if len(maxKey_list) == 0:
        maxKey_list.append(v[0])
      lastKey = len(maxKey_list) - 1

      if recurce_post(v, scheList):
        break
      else :
        continue

def recurce_post(current_v, sche_list):
  global maxKey_list, scheDict

  send_count = 0

  if current_v[0] in maxKey_list and current_v[1][1] > 0:
    print current_v[0]+" post to "+current_v[1][0]
    if current_v[1][0] != NodeInfo.getMainKey() :
      calculator_queue(current_v[1][0], sche_list, "+")
    send_count = calculator_queue(current_v[0], sche_list, "-")

    ## Pass to next function
    TopologyTable.slotPostControl(current_v[1][0], current_v[0], send_count)

    return True
  elif current_v[0] in maxKey_list and current_v[1][1] == 0:
    for v in scheList :
      if v[1][0] in maxKey_list[lastKey] and v[1][2] > 1:
        if v[0] not in maxKey_list:
          maxKey_list.append(v[0])
        break
    if check_queue(current_v[0]):
      return True
    return False
  elif current_v[1][0] is maxKey_list[lastKey] and current_v[1][1] > 0:
    print current_v[0]+" post to *"+current_v[1][0]
    if current_v[1][0] != NodeInfo.getMainKey() :
      calculator_queue(current_v[1][0], sche_list, "+")
    send_count = calculator_queue(current_v[0], sche_list, "-")

    ## Pass to next function
    TopologyTable.slotPostControl(current_v[1][0], current_v[0], send_count)

    return True
  else :
    return False


def calculator_queue(current_v, sche_list, operator_flag):
  global scheList, scheDict
  if current_v[0] != NodeInfo.getMainKey():
    temp = scheDict[current_v]
    lq = temp[1]
    gq = temp[2]
    send_count = temp[3]
    if operator_flag is "-" :
      lq -= 1
      gq -= 1
      scheDict[current_v] = [temp[0], lq, gq, send_count+1]
    elif operator_flag is "+" :
      lq += 1
      scheDict[current_v] = [temp[0], lq, gq, send_count]

    if lq == 0 and gq == 0:
      print "Delete "+current_v[0]
      scheDict.pop(current_v[0])
      if current_v[0] in maxKey_list:
        maxKey_list.remove(current_v[0])
    
    if operator_flag is "-" :
      return send_count
  
  scheList = sorted(scheDict.items(), lambda x, y: cmp(x[1][2], y[1][2]), reverse=True)

def check_queue(current_v):
  global scheDict, maxKey_list
  if current_v != NodeInfo.getMainKey():
    temp = scheDict[current_v]
    lq = temp[1]
    gq = temp[2]
    if lq == 0 and gq == 0:
      print "Delete *"+current_v[0]
      scheDict.pop(current_v[0])
      if current_v[0] in maxKey_list:
        maxKey_list.remove(current_v[0])
