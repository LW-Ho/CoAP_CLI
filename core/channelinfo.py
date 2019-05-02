node_channel_list = []

def initial_channel_list(Flag):
  if Flag :
    node_channel_list = [[0 for i in range(16)] for j in range(141)]
  
def set_channel_list(childKey, parentKey, slot_numbers):
  while slot_numbers > 0 :
    for j in range(10,151) :
      for i in range(16) :
        if node_channel_list[j][i] is not 0:
          strTemp = node_channel_list[j][i].split(',')
          # check child and parent both are in node_channel_list ?
          if childKey in strTemp:
            break
          if parentKey in strTemp:
            break
          node_channel_list[j][i] = childKey+","+parentKey
          slot_numbers -= 1
          return j, i
        else :
          node_channel_list[j][i] = childKey+","+parentKey
          slot_numbers -= 1
          return j, i

# slot_offset is j
# channel_offset is i
def get_channel_list(childKey, parentKey):
  current_Str = childKey+","+parentKey
  for j in range(10,151) :
      for i in range(16) :
        if node_channel_list[j][i] is not 0:
          strTemp = node_channel_list[j][i]
          if cmp(current_Str, strTemp) is 0:
            # if not set, will return 0
            node_channel_list[j][i] = 0
            return j, i
  
  return 0, 0
 

def remove_channel_list(slot_offset, channel_offset):
  node_channel_list[slot_offset][channel_offset] = 0
  return True