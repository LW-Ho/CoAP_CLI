import subprocess, sys
import threading

class StartObserve(threading.Thread):
  def __init__(self, node, resource):
    threading.Thread.__init__(self)
    self.node = node
    self.resource = resource
    return

  def run(self):
    get_cmd = 'coap -o \"coap://['+self.node+']:5683/g/'+self.resource+'\"'
    try:
      subprocess.call(get_cmd, shell=True)
      # retcode = subprocess.call(get_cmd)
      # log.debug(retcode)
      return
    except:
      print "Not success for send out.\n"
      pass

  def stop(self):
    subprocess.terminate()
    self._is_running = False

  def getName(self):
    print self.node