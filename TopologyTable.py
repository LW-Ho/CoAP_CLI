topology_table = []

def set_table(topology_List):
  topology_table = topology_List

def get_table():

  if len(topology_table) is 0 :
    # return false
    return []
  else :
    print "Got it ~~"
    return topology_table