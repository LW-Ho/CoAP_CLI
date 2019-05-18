import RestCoAP
import core.channelinfo as ChannelInfo
import core.nodeinfo as NodeInfo

# for parent node to post other child node.
def PostQuery(childKey, parentKey, timeslot_offset, channel_offset, del_timeslot, delFlag):
  resource = "slotframe"

  # TX = 1 / RX = 2
  if delFlag is 1:
    query1 = "slot="+str(timeslot_offset)+"&chanl="+str(channel_offset)+"&numbers="+str(1)+"&link=TX"
    RestCoAP.postQueryToNode(childKey, resource, query1)
    query2 = "slot="+str(timeslot_offset)+"&chanl="+str(channel_offset)+"&numbers="+str(1)+"&link=RX"
    RestCoAP.postQueryToNode(parentKey, resource, query2) # send by self.

  elif delFlag is 2:
    delquery = "delslot="+str(del_timeslot)+"&delnumbers="+str(1)

    query1 = "slot="+str(timeslot_offset)+"&chanl="+str(channel_offset)+"&numbers="+str(1)+"&link=TX"+delquery
    RestCoAP.postQueryToNode(childKey, resource, query1)
    query2 = "slot="+str(timeslot_offset)+"&chanl="+str(channel_offset)+"&numbers="+str(1)+"&link=RX"+delquery
    RestCoAP.postQueryToNode(parentKey, resource, query2) # send by self.

  else :
    # nothing
    pass