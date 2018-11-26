import time
from coapthon.client.helperclient import HelperClient

# coap get "coap://[fd00::212:4b00:615:a736]:5683/g/sht21?pp=2&thd=20"
port = 5683

def postQueryToNode(node,resource,query):
  query = "?"+query
  resource = "g/"+resource+query
  # try:
  coap_client = HelperClient(server=(node, port))
  start = time.time()
  coap_client.post(path=resource, payload='' ,timeout=60)
  coap_client.stop()
  elapsed = time.time() - start
  print "%s \nSuccessful delivery, %.2f seconds." %(node, elapsed)
  return elapsed
  # except:
  #   print "Did not successfully send out."
  #   pass  

def postToAllNode(List,resource,query):
  query = "?"+query
  resource = "g/"+resource+query

  for node in List:
    try:
      coap_client = HelperClient(server=(node, port))
      start = time.time()
      #coap_client.post(resource, '')
      coap_client.post(path=resource, payload='' ,timeout=60)
      coap_client.stop()
      elapsed = time.time() - start
      print "%s \nSuccessful delivery, %.2f seconds." %(node, elapsed)

    except:
      print "Did not successfully send out."
      pass

  return
  