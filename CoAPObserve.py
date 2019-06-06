import threading
import sys
from coapthon.client.helperclient import HelperClient

from MoteData import MoteData
import logging
log = logging.getLogger("CoAPObserve")

class CoAPObserve(threading.Thread):
  def __init__(self, node, resource, port=5683, group=None, target=None, kwargs=None, verbose=None, object_callback=None):
    threading.Thread.__init__(self, group=group, target=target, name=node, verbose=verbose)
    self.coap_client = None
    self.flag = True
    self.cancel_observe = False
    self.counter_Check = 0
    self.counter_Observing = 0
    self.kwargs = kwargs
    self.node = node
    self.resource = resource
    self.port = port
    self.object_callback = object_callback
    self.response = None
    return

  def message_callback(self, response):
        """
        :type response: coapthon.messages.response.Response
        """
        if response is not None:
          if self.flag:
            self.flag = False
            print("")
            log.debug("Got new message -> {0}".format(self.node))
            if log.isEnabledFor(logging.DEBUG):
                packet_content = ":".join("{:02x}".format(ord(c)) for c in response.payload)
                log.debug(packet_content)
            log.debug("Payload length: {0}".format(len(response.payload)))
            log.debug("=================================")
            print(">")

          # will upload data to mysql server.
          try :
            mote_data = MoteData.make_from_bytes(response.source[0], response.payload)
            # MoteData.make_from_bytes(response.source[0], response.payload, 1) # need save the value, if refresh topology will get the value to check node local queue.
            if mote_data is not None and self.object_callback is not None:
              self.counter_Observing+=1 # counter callback.
              self.object_callback(mote_data) # callback to main function.
          except :
            self.flag = True
            self.coap_client.cancel_observing(response, self.flag)
            self.coap_client.close()
            log.info("Unexpected error: {0}".format(sys.exc_info()[0]))
            #self.stdout.write("Unexpected error:", sys.exc_info()[0])
            print("")
          else :
            if self.cancel_observe:
              """
              Delete observing on the remote server.
              :param response: the last received response
              :param explicit: if explicitly cancel using token
              :type send_rst: bool
              """
              self.coap_client.cancel_observing(response, self.cancel_observe) # send RST packet by CoAP.
              self.coap_client.close()
              self.flag = True
              
  def run(self):
    log.info("CoAP Observe \"{0}\" started.".format(self.name))
    print("")
    self.coap_client = HelperClient(server=(self.node, self.port))
    self.coap_client.observe(path=self.resource, callback=self.message_callback)
    return

  def stop(self):
    log.info("Stoping CoAP Observe \"{0}\" .".format(self.name))
    if self.coap_client is not None:
      try:
        self.flag = True
        self.cancel_observe = True
        #self.coap_client.close()
      except:
        print("Cannot join thread before it is started...")
      return

  def printName(self):
    log.info("Node Name : {0}".format(self.node))
    #print self.node

  def getName(self):
    return self.node

  def getFlag(self):
    return self.flag

  def getCountOb(self):
    return self.counter_Observing

  def getCountCk(self):
    return self.counter_Check

  def saveCountCk(self, countOb):
    self.counter_Check = countOb
  
  def stopOb(self):
    self.cancel_observe = True

  def checkOb(self):
    return self.cancel_observe
    
    