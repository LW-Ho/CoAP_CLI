import logging
log = logging.getLogger("REST_CoAP")
import sys

import time
from coapthon.client.helperclient import HelperClient
# coap get "coap://[fd00::212:4b00:615:a736]:5683/g/sht21?pp=2&thd=20"
port = 5683

def postPayloadToNode(node, resource, payload_data):
  resource = "res/"+resource
  log.info("{0} : {1}, payload -> {2}".format(node, resource, payload_data))
  try:
    coap_client = HelperClient(server=(node, port))
    start = time.time()
    coap_client.post(path=resource, payload=payload_data ,timeout=30)
    coap_client.close()
    elapsed = time.time() - start
    log.info("{} successful delivery, {:.2f} seconds. ".format(node, elapsed-1))
    return True
  except:
    coap_client.close()
    log.info("{0} did not successfully send out, retry again.".format(node))
    return False

def postQueryToNode(node,resource,query):
  query = "?"+query
  resource = "res/"+resource+query
  try:
    coap_client = HelperClient(server=(node, port))
    start = time.time()
    coap_client.post(path=resource, payload='' ,timeout=30)
    coap_client.close()
    elapsed = time.time() - start
    log.info("{} successful delivery, {0:.2f} seconds. ".format(node, elapsed-1))
  except:
    coap_client.close()
    log.info("{0} did not successfully send out, retry again.".format(node))

def postToAllNode(List,resource,query):
  query = "?"+query
  resource = "res/"+resource+query

  for node in List:
    try:
      coap_client = HelperClient(server=(node, port))
      start = time.time()
      coap_client.post(path=resource, payload='' ,timeout=30)
      coap_client.close()
      elapsed = time.time() - start
      log.info("{} successful delivery, {0:.2f} seconds. ".format(node, elapsed-1))

    except:
      coap_client.close()
      log.info("{0} did not successfully send out, retry again.".format(node))
      pass

  return