import subprocess, sys
import time

# coap get "coap://[fd00::212:4b00:615:a736]:5683/g/sht21?pp=2&thd=20"

def postQueryToNode(node,resource,query):
  get_cmd = 'echo -n \'POST\' | coap post \"coap://['+node+']:5683/g/'+resource+'?'+query+'\"'
  try:
    start = time.time()
    retcode = subprocess.call(get_cmd, shell=True)
    elapsed = time.time() - start
    print "Successful delivery, %.2f seconds." %(elapsed)
    return elapsed
  except:
    print "Not success for send out."
    pass
    

def postToAllNode(List,resource,query):
  for node in List:
    get_cmd = 'echo -n \'POST\' | coap post \"coap://['+node+']:5683/g/'+resource+'?'+query+'\"'
    try:
      start = time.time()
      retcode = subprocess.call(get_cmd, shell=True)
      elapsed = time.time() - start
      print "%s \nSuccessful delivery, %.2f seconds." %(node, elapsed)
      
    except:
      print "Not success for send out."
      pass

  return
  