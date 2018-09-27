import subprocess, sys

# coap get "coap://[fd00::212:4b00:615:a736]:5683/g/sht21?pp=2&thd=20"

def getToNode(node,resource):
  get_cmd = 'coap get \"coap://['+node+']:5683/g/'+resource+'\"'
  try:
    retcode = subprocess.call(get_cmd, shell=True)
  except:
    print "Not success for send out."
  
def getQueryToNode(node,resource,query):
  get_cmd = 'coap get \"coap://['+node+']:5683/g/'+resource+'?'+query+'\"'
  try:
    retcode = subprocess.call(get_cmd, shell=True)
  except:
    print "Not success for send out."