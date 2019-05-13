import logging
log = logging.getLogger("NodeLocalQueue")
import sys

import time
from coapthon.client.helperclient import HelperClient
# coap get "coap://[fd00::212:4b00:615:a736]:5683/g/sht21?pp=2&thd=20"
from MoteData import MoteData
import core.nodeinfo as NodeInfo

port = 5683
nodeName = None
return_flag = 1

def message_callback(response):
  global return_flag
  """
  :type response: coapthon.messages.response.Response
  """
  if response is not None:
    print("")
    print("Got new message -> {0}".format(nodeName))
    
    packet_content = ":".join("{:02x}".format(ord(c)) for c in response.payload)
    print(packet_content)
    print("Payload length: {0}".format(len(response.payload)))
    print("=================================")
    print(">")
    try :
      MoteData.make_from_bytes(response.source[0], response.payload, 1)
      return_flag = 0
    except :
      print("Unexpected error: {0}".format(sys.exc_info()[0]))
      print("")

def getNodeLocalQueue(node):
  global nodeName, return_flag
  return_flag = 1 # to initialized value.
  
  nodeName = node
  print nodeName
  try:
    coap_client = HelperClient(server=(node, port))
    start = time.time()
    coap_client.get(path="res/bcollect", callback=message_callback, timeout=60)

    while (return_flag) :
      elapsed = time.time() - start
      print 'Watting time : %2.2f\r' % elapsed,
      if elapsed > 60 :
        coap_client.close()
        coap_client.get(path="res/bcollect", callback=message_callback, timeout=60)
        start = time.time()

    coap_client.close()
    elapsed = time.time() - start
    print "%s  successful delivery, %.2f seconds." %(node, elapsed)
    local_queue_numbers = NodeInfo.getNodeLQ(node)
    print "Got the local queue : %s " %(str(local_queue_numbers))
    return int(local_queue_numbers)
  except:
    if coap_client is not None:
      coap_client.close()
    print node+" did not successfully send out."

