import subprocess, sys

# coap get "coap://[fd00::212:4b00:615:a736]:5683/g/sht21?pp=2&thd=20"

def postQueryToNode(node,resource,query):
  get_cmd = 'echo -n \'POST\' | coap post \"coap://['+node+']:5683/g/'+resource+'?'+query+'\"'
  try:
    retcode = subprocess.call(get_cmd, shell=True)
    print "Successful delivery."
    return
  except:
    print "Not success for send out."
    pass
    

def postToAllNode(List,resource,query):
  for node in List:
    get_cmd = 'echo -n \'POST\' | coap post \"coap://['+node+']:5683/g/'+resource+'?'+query+'\"'
    try:
      retcode = subprocess.call(get_cmd, shell=True)
      print "%s \nSuccessful delivery." %(node)
      
    except:
      print "Not success for send out."
      pass

  return