import sys
from coapthon.client.helperclient import HelperClient

from core.MoteData import MoteData
import logging
log = logging.getLogger("CoAP REST Engine")

class NodeInfo():
  def __init__(self, node, resource, query, port=5683):
    self.coap_client = None
    self.node = node
    self.resource = "res/"+resource
    self.query = "?slot="+query
    self.port = port
    self.nodeInfo = None
    return

  def message_get(self, response):
    if response is not None:
      log.debug("Got new message -> {0}".format(self.node))
      if log.isEnabledFor(logging.DEBUG):
          packet_content = ":".join("{:02x}".format(ord(c)) for c in response.payload)
          log.debug(packet_content)
      log.debug("Payload length: {0}".format(len(response.payload)))
      log.debug("=================================")

      try:
        # created dictionary.
        mote_data = MoteData.make_from_bytes(response.source[0], response.payload)
        if mote_data is not None:
          # to copy dictionary to nodeInfo
          self.nodeInfo = mote_data
      except:
        log.info("Unexpected error: {0}".format(sys.exc_info()[0]))
    

  def getNode(self):
    try:
      coap_client = HelperClient(server(self.node, self.port))
      coap_client.get(path=self.resource, callback=self.message_get, timeout=60)
      log.info("Get successful.")
    except:
      coap_client.stop()
      log.info("Failed.")

  def postNode(self, slot):
    self.resource = self.resource+self.query
    try:
      coap_client = HelperClient(server(self.node, self.port))
      coap_client.post(path=self.resource, payload='', callback=self.message_get, timeout=60)
      log.info("Get successful.")
    except:
      coap_client.stop()
      log.info("Failed.")