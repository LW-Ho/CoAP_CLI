import logging
log = logging.getLogger("NodeLocalQueue")
import sys

import time
from coapthon.client.helperclient import HelperClient
# coap get "coap://[fd00::212:4b00:615:a736]:5683/g/sht21?pp=2&thd=20"
from MoteData import MoteData

port = 5683
nodeName = None
local_queue_numbers = '1'
return_flag = 1

def message_callback(response):
  global local_queue_numbers, return_flag
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

  return_flag = 0

  # will upload data to mysql server.
  try :
    local_queue_numbers = MoteData.make_from_bytes(response.source[0], response.payload, 1)
  except :
    print("Unexpected error: {0}".format(sys.exc_info()[0]))
    #self.stdout.write("Unexpected error:", sys.exc_info()[0])
    print("")

def getNodeLocalQueue(node):
  global nodeName, return_flag
  return_flag = 1
  
  nodeName = node
  print nodeName
  # try:
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
  print "Got the local queue : %s " %(str(local_queue_numbers))
  return_flag = 1
  return int(local_queue_numbers)
  # except:
  #   if coap_client is not None:
  #     coap_client.stop()
   # print node+" did not successfully send out."

