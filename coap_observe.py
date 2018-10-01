import subprocess, sys
import os
import signal
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
      self.coapProcess = subprocess.Popen(get_cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
      # retcode = subprocess.call(get_cmd)
      # log.debug(retcode)
    except:
      print "Not success for send out.\n"
      pass

  def stop(self):
    try:
      # self.coapProcess.send_signal(signal.SIGINT)
      # self.coapProcess.terminate()
      os.killpg(os.getpgid(self.coapProcess.pid), signal.SIGTERM)
      self._is_running = False
    except:
      print "Error of terminate()"
      return
    
  def printName(self):
    print self.node

  def getName(self):
    return self.node
    