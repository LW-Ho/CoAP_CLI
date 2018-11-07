#import subprocess, sys
import time
from coapthon.client.helperclient import HelperClient

# coap get "coap://[fd00::212:4b00:615:a736]:5683/g/sht21?pp=2&thd=20"
port = 5683

def postQueryToNode(node,resource,query):
  query = "?"+query
  resource = "g/"+resource+query
  #log.info("CoAP Observe \"{0}\" started.".format(self.name))
  try:
    coap_client = HelperClient(server=(node, port))
    start = time.time()
    coap_client.post(path=resource)
    elapsed = time.time() - start
    print "%s \nSuccessful delivery, %.2f seconds." %(node, elapsed)
    return elapsed
  except:
    print "Did not successfully send out."
    pass
  # get_cmd = 'echo -n \'POST\' | coap post \"coap://['+node+']:5683/g/'+resource+'?'+query+'\"'
  # try:
  #   start = time.time()
  #   retcode = subprocess.call(get_cmd, shell=True)
  #   elapsed = time.time() - start
  #   print "%s \nSuccessful delivery, %.2f seconds." %(node, elapsed)
  #   return elapsed
  # except:
  #   print "Did not successfully send out."
  #   pass
    

def postToAllNode(List,resource,query):
  for node in List:
    get_cmd = 'echo -n \'POST\' | coap post \"coap://['+node+']:5683/g/'+resource+'?'+query+'\"'
    try:
      start = time.time()
      retcode = subprocess.call(get_cmd, shell=True)
      elapsed = time.time() - start
      print "%s \nSuccessful delivery, %.2f seconds." %(node, elapsed)
      
    except:
      print "Did not successfully send out."
      pass

  return
  