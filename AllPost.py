import threading
import RestCoAP
import re
import time

import logging
log = logging.getLogger("AllPost")

class AutoPost(threading.Thread):
  def __init__(self, nodeKey, payload_data, resource, endASN, node=None, group=None, target=None, verbose=None):
    threading.Thread.__init__(self, group=group, target=target, name=nodeKey, verbose=verbose)
    self.nodeKey = nodeKey
    self.payload_data = payload_data
    self.resource = resource
    self.endASN = endASN
    self.signal = False
    return

  def run(self):
    log.info("Starting Post to {0} with Payload Data {1} .".format(self.nodeKey, self.payload_data))
    while self.signal is False:
      temp_payload = self.cut_payload(self.payload_data, 48)
      for i in range(len(temp_payload)):
        time.sleep(0.1)
        if i == 0:
          if self.endASN is not 0:
            self.signal = RestCoAP.postPayloadToNode(self.nodeKey, self.resource+"&option=2", temp_payload[i])
          else :
            self.signal = RestCoAP.postPayloadToNode(self.nodeKey, self.resource+"?option=2", temp_payload[i])
        else :
          self.signal = RestCoAP.postPayloadToNode(self.nodeKey, self.resource, temp_payload[i])
    if self.signal is True:
      self.stop()
      
  def stop(self):
    log.info("Stoping Post Payload to {0} .".format(self.nodeKey))

  def cut_payload(self, payload, length):
    payloadArr = re.findall('.{'+str(length)+'}', payload)
    payloadArr.append(payload[(len(payloadArr)*length):])
    return payloadArr
