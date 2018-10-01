import subprocess, sys
import threading

class StartObserve(threading.Thread):
  def __init__(self, node, resource):
    threading.Thread.__init__(self)
    self.node = node
    self.resource = resource
    self.coapProcess = None
    return

  def run(self):
    get_cmd = 'coap -o \"coap://['+self.node+']:5683/g/'+self.resource+'\"'
    try:
      self.coapProcess = subprocess.call(get_cmd, shell=True)
      # retcode = subprocess.call(get_cmd)
      # log.debug(retcode)
      return
    except:
      print "Not success for send out.\n"
      pass

  def stop(self):
    try:
      if self.coapProcess is not None:
        self.coapProcess.send_signal(signal.SIGINT)
      else:
        print "Error of send_signal"
    except:
      print "Error of terminate()"
    self._is_running = False

  def printName(self):
    print self.node

  def getName(self):
    return self.node
    