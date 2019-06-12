import logging
log = logging.getLogger("REST_CoAP")
import sys

import time
from coapthon.client.helperclient import HelperClient
# coap get "coap://[fd00::212:4b00:615:a736]:5683/g/sht21?pp=2&thd=20"
port = 5683

def postPayloadToNode(node, resource, payload_data):
  resource = "res/"+resource
  try:
    coap_client = HelperClient(server=(node, port))
    start = time.time()
    coap_client.post(path=resource, payload=payload_data ,timeout=20)
    coap_client.close()
    elapsed = time.time() - start
    print "%s  successful delivery, %.2f seconds." %(node, elapsed-1)
    return True
  except:
    coap_client.close()
    print node+" did not successfully send out, retry again."
    return False

def postQueryToNode(node,resource,query):
  query = "?"+query
  resource = "res/"+resource+query
  try:
    coap_client = HelperClient(server=(node, port))
    start = time.time()
    coap_client.post(path=resource, payload='' ,timeout=60)
    coap_client.close()
    elapsed = time.time() - start
    print "%s  successful delivery, %.2f seconds." %(node, elapsed-1)
  except:
    coap_client.close()
    print node+" did not successfully send out."

def postToAllNode(List,resource,query):
  query = "?"+query
  resource = "res/"+resource+query

  for node in List:
    try:
      coap_client = HelperClient(server=(node, port))
      start = time.time()
      coap_client.post(path=resource, payload='' ,timeout=60)
      coap_client.close()
      elapsed = time.time() - start
      print "%s  successful delivery, %.2f seconds." %(node, elapsed-1)

    except:
      coap_client.close()
      print node+" did not successfully send out."
      pass

  return