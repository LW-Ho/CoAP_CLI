import time
from coapthon.client.helperclient import HelperClient
# coap get "coap://[fd00::212:4b00:615:a736]:5683/g/sht21?pp=2&thd=20"
from MoteData import MoteData

port = 5683
nodeName = None
local_queue_numbers = 1

def message_callback(self, response):
  global local_queue_numbers
  """
  :type response: coapthon.messages.response.Response
  """
  if response is not None:
    print("")
    log.debug("Got new message -> {0}".format(nodeName))
    if log.isEnabledFor(logging.DEBUG):
        packet_content = ":".join("{:02x}".format(ord(c)) for c in response.payload)
        log.debug(packet_content)
    log.debug("Payload length: {0}".format(len(response.payload)))
    log.debug("=================================")
    print(">")

  # will upload data to mysql server.
  try :
    local_queue_numbers = MoteData.make_from_bytes(response.source[0], response.payload, 1)
  except :
    log.info("Unexpected error: {0}".format(sys.exc_info()[0]))
    #self.stdout.write("Unexpected error:", sys.exc_info()[0])
    print("")

def getNodeLocalQueue(node):
  global nodeName
  nodeName = node
  resource = "res/bcollect"
  try:
    coap_client = HelperClient(server=(node, port))
    start = time.time()
    coap_client.post(path=resource, payload='', callback=message_callback, timeout=60)
    coap_client.stop()
    elapsed = time.time() - start
    print "%s  successful delivery, %.2f seconds." %(node, elapsed)
    print "Got the local queue : %d " %(local_queue_numbers)
    return local_queue_numbers
  except:
    coap_client.stop()
    print node+" did not successfully send out."

