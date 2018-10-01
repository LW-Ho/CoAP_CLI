import threading
import logging

class StartObserve(threading.Thread):
  def __init__(self, node, resource):
    threading.Thread.__init__(self)
    self.node = node
    self.resource = resource
    return

  def run(self):
    get_cmd = 'coap -o \"coap://['+self.node+']:5683/g/'+self.resource+'\"'
    try:
      retcode = subprocess.call(get_cmd, shell=True)
      # log.debug(retcode)
      return
    except:
      log.debug("Not success for send out."
      pass

  def stop(self):
    self._is_running = False