node_channel_list = []

def initial_channel_list(Flag):
  global node_channel_list
  if Flag :
    node_channel_list = [[0 for i in range(16)] for j in range(151)]
  
def set_channel_list(childKey, parentKey, slot_numbers):
  global node_channel_list
  if slot_numbers > 0:
    for j in range(10,151) :
      for i in range(16) :
        # print node_channel_list[j][i]
        if node_channel_list[j][i] is not 0:
          strTemp = node_channel_list[j][i].split(',')

          # check child and parent both are in node_channel_list ?
          if childKey in strTemp:
            break
          if parentKey in strTemp:
            break
          continue

        else :
          node_channel_list[j][i] = childKey+","+parentKey
          slot_numbers = slot_numbers - 1
          print "slot offset : "+str(j)+", channel offset : "+str(i)
          #print j, i
          return j, i

# slot_offset is j
# channel_offset is i
def get_channel_list(childKey, parentKey):
  global node_channel_list
  current_Str = childKey+","+parentKey
  for j in range(10,151) :
    for i in range(16) :
      if node_channel_list[j][i] is not 0:
        strTemp = node_channel_list[j][i]
        if cmp(current_Str, strTemp) is 0:
          # if not set, will return 0
          print "IN Get_channel_list"
          node_channel_list[j][i] = 0
          return j, i
  
  return 0, 0

def peek_get_channel_list(childKey, parentKey, globalQu):
  global node_channel_list
  temp_count = 1
  current_Str = childKey+","+parentKey
  for j in range(10,151) :
    for i in range(16) :
      if node_channel_list[j][i] is not 0:
        strTemp = node_channel_list[j][i]
        if cmp(current_Str, strTemp) is 0:
          if temp_count == globalQu :
            temp_count += 1
            print "IN Get_channel_list"
            return j, i
          else :
            temp_count += 1
            break

  return 0, 0

def peek_set_channel_list(childKey, parentKey, slot_offset, channel_offset, globalQu):
  GQ_count = 0
  if globalQu is None:
    globalQu = 1
  current_Str = childKey+","+parentKey
  while (globalQu != GQ_count) :
    if node_channel_list[slot_offset][channel_offset] is not 0:
      strTemp = node_channel_list[slot_offset][channel_offset]
      if cmp(current_Str, strTemp) is 0:
        GQ_count += 1
        if (globalQu == GQ_count) :
          return True  
      else :
        return False
    else :
      return False

def peek_next_parent_channel_list(old_parentKey, del_slot, del_channel):
  for j in range(del_slot,151) :
    for i in range(16) :
      if node_channel_list[j][i] is not 0:
        strTemp = node_channel_list[j][i].split(',')
        if cmp(old_parentKey, strTemp[0]) is 0:
          print "IN Get_channel_list"
          return strTemp[1], j, i
        else :
          break

  return 0, 0, 0

def check_parent_changed(childKey, parentKey):
  global node_channel_list
  for j in range(10,151) :
    for i in range(16) :
      # print node_channel_list[j][i]
      if node_channel_list[j][i] is not 0:
        strTemp = node_channel_list[j][i].split(',')

        # check child and parent both are in node_channel_list ?
        if childKey in strTemp[0]:
          if parentKey not in strTemp[1]:
            print "got the old setting"
            # the slot and channel will delete.
            return j, i
  return 0, 0
  

 

def remove_channel_list(slot_offset, channel_offset):
  global node_channel_list
  strTemp = node_channel_list[slot_offset][channel_offset].split(',')
  node_channel_list[slot_offset][channel_offset] = 0
  return strTemp[1]