import logging
log = logging.getLogger("NodeLocalQueue")
import sys

import time
from coapthon.client.helperclient import HelperClient
# coap get "coap://[fd00::212:4b00:615:a736]:5683/g/sht21?pp=2&thd=20"
from MoteData import MoteData
port = 5683
local_queue_numbers = 1

def postQueryToNode(node,resource,query):
  query = "?"+query
  resource = "res/"+resource+query
  flag = 0
  while flag == 0 :
    try:
      coap_client = HelperClient(server=(node, port))
      start = time.time()
      coap_client.post(path=resource, payload='' ,timeout=60)
      coap_client.stop()
      elapsed = time.time() - start
      print "%s  successful delivery, %.2f seconds." %(node, elapsed)
      flag = 1
    except:
      coap_client.stop()
      print node+" did not successfully send out, retry..."

def postToAllNode(List,resource,query):
  query = "?"+query
  resource = "res/"+resource+query

  for node in List:
    try:
      coap_client = HelperClient(server=(node, port))
      start = time.time()
      #coap_client.post(resource, '')
      coap_client.post(path=resource, payload='' ,timeout=60)
      coap_client.stop()
      elapsed = time.time() - start
      print "%s  successful delivery, %.2f seconds." %(node, elapsed)

    except:
      coap_client.stop()
      print node+" did not successfully send out."
      pass

  return