topology_table = []

def set_table(topology_List):
  topology_table = topology_List

def get_table(void):

  if len(topology_table) is 0 :
    # 傳回去當作false
    return 0
  else :
    return topology_table