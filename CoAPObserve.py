import threading
from coapthon.client.helperclient import HelperClient

from MoteData import MoteData
import logging
log = logging.getLogger("CoAPObserve")

class CoAPObserve(threading.Thread):
  def __init__(self, node, resource, port=5683, group=None, target=None, kwargs=None, verbose=None, object_callback=None):
    threading.Thread.__init__(self, group=group, target=target, name=node, verbose=verbose)
    self.coap_client = None
    self.flag = True
    self.kwargs = kwargs
    self.node = node
    self.resource = resource
    self.port = port
    self.object_callback = object_callback
    return

  def message_callback(self, response):
        """
        :type response: coapthon.messages.response.Response
        """
        if response is not None:
          if self.flag:
            self.flag = False
            log.debug("Got new message")
            if log.isEnabledFor(logging.DEBUG):
                packet_content = ":".join("{:02x}".format(ord(c)) for c in response.payload)
                log.debug(packet_content)
            log.debug("Payload length: {0}".format(len(response.payload)))
            log.debug("=================================")
          
          # will upload data to mysql server.
          mote_data = MoteData.make_from_bytes(response.source[0], response.payload)
          if mote_data is not None and self.object_callback is not None:
              self.object_callback(mote_data)

  def run(self):
    log.info("CoAP Observe \"{0}\" started.".format(self.name))
    self.coap_client = HelperClient(server=(self.node, self.port))
    self.coap_client.observe(path=self.resource, callback=self.message_callback)
    return
    # get_cmd = 'coap -o \"coap://['+self.node+']:5683/g/'+self.resource+'\"'
    # try:
    #   self.coapProcess = subprocess.Popen(get_cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    # except:
    #   print "Not success for send out.\n"
    #   pass

  def stop(self):
    log.info("Stoping CoAP Observe \"{0}\" .".format(self.name))
    if self.coap_client is not None:
      self.flag = True
      self.coap_client.stop()
    else :
      log.info("Deleted Done !")
      return

    # try:
    #   os.killpg(os.getpgid(self.coapProcess.pid), signal.SIGTERM)
    #   self._is_running = False
    # except:
    #   print "Error of terminate()"
    #   return
    
  def printName(self):
    log.info("Node Name : {0}".format(self.node))
    #print self.node

  def getName(self):
    return self.node
    