topology_table = []
global_counter = 0
testing_flag = 0

def set_table(host, topology_List):
  dictTemp = {}

  for item in topology_List:
    print item
    if item[0] in dictTemp:
      dictTemp[item[0]].append(item[1])
    else:
      dictTemp[item[0]] = [item[1]]

  topology_print(dictTemp, host)

def topology_print(dictTemp, host):
  global global_counter
  local_queue = 1
  get_queue = 0
  for mainKey in dictTemp.keys():
    if mainKey in host:
      print mainKey # host
      global_counter += 1
      for childKey in dictTemp.get(mainKey):

        # host's child is other node's parent.
        if childKey in dictTemp.keys(): 
          global_counter += 1

          print "--"+" 1 "+childKey
          get_queue = parentAndChild(childKey, dictTemp, 1)

          
          dictTemp.pop(childKey)
          if testing_flag :
            print childKey+" global queue "+str(get_queue+local_queue)
        # only child
        else: 
          global_counter += 1
          print "--"+" 1 "+childKey
  if testing_flag :
    print "All topology global queue "+str(global_counter)


def parentAndChild(parentKey, dictTemp, temp_counter):
  global global_counter
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
      if testing_flag :
        print childKey+" global queue "+str(local_queue)

    # end of child.
    else :
      global_counter += 1
      local_queue += 1
      temp_str = ""
      for index in range(0,temp_counter+1):
        temp_str = temp_str+"--"
      print temp_str+" "+str(temp_counter+1)+" "+childKey

  return local_queue
