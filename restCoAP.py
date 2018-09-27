import subprocess, sys
import threading

# coap get "coap://[fd00::212:4b00:615:a736]:5683/g/sht21?pp=2&thd=20"
 
def getQueryToNode(node,resource,query):
  get_cmd = 'coap get \"coap://['+node+']:5683/g/'+resource+'?'+query+'\"'
  try:
    retcode = subprocess.call(get_cmd, shell=True)
    print retcode
  except:
    print "Not success for send out."

def getToAllNode(List,resource,query):
  for node in List:
    get_cmd = 'coap get \"coap://['+node+']:5683/g/'+resource+'?'+query+'\"'
    try:
      retcode = subprocess.call(get_cmd, shell=True)
      print retcode
    except:
      print "Not success for send out."

def startObserve(node,resource):
  get_cmd = 'coap -o \"coap://['+node+']:5683/g/'+resource+'\"'
  try:
    retcode = subprocess.call(get_cmd, shell=True)
    print retcode
  except:
    print "Not success for send out."