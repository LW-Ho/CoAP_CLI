import threading
import time
from coapthon.client.helperclient import HelperClient
from CoAPObserve import CoAPObserve

import logging
log = logging.getLogger("CoAPObserve")

class AutoOb(threading.Thread):
  def __init__(self, mote_lists, mote_observe_lists, node=None, group=None, target=None, verbose=None, autoOb_callback=None, object_callback=None):
    threading.Thread.__init__(self, group=group, target=target, name=node, verbose=verbose)
    self.auto_ob = None
    self.record_counter = 0
    self.mote_lists = mote_lists
    self.mote_observe_lists = mote_observe_lists
    self.autoOb_callback = autoOb_callback
    self.object_callback = object_callback
    return

  def run(self):
    log.info("Starting auto observing nodes.")
    print("")
    while True:
      s1 = set(self.mote_lists)
      temp = []

      for obnode in self.mote_observe_lists: # to change element type, then save to oher list. (CoAP to string)
        temp.append(obnode.getName())
      s2 = set(temp)

      result = list(s1.difference(s2)) # compare list,we can know that is not observing.
      # try :
      for node in result:
        coapObserve = CoAPObserve(node=node, resource="g/bcollect", object_callback=self.object_callback)
        coapObserve.printName()
        coapObserve.start()
        self.mote_observe_lists.append(coapObserve)

      time.sleep(60) # sleep 1mins.
      log.info("Observe ALL Done.")

      self.mote_lists = self.autoOb_callback(self.mote_observe_lists)

      for node in self.mote_observe_lists:
        if (node.getCountOb() - node.getCountCk()) > 5: # 5 is offset number.
          node.saveCountCk(node.getCountOb()) # record fresh count number.
          continue
        else:
          node.stop()
          node.printName()
          node.start()

      # except :
      #   log.info("Do not found moteAddress text.")
        
    return

  def stop(self):
    log.info("Stoping auto observing nodes.")
    return
