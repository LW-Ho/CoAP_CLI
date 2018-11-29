import threading
import time
from coapthon.client.helperclient import HelperClient
from CoAPObserve import CoAPObserve
from GetMotes import getAllMotes

import logging
log = logging.getLogger("CoAPObserve")

class AutoOb(threading.Thread):
  def __init__(self, mote_lists, mote_observe_lists, countDown=None, node=None, group=None, target=None, verbose=None, autoOb_callback=None, object_callback=None):
    threading.Thread.__init__(self, group=group, target=target, name=node, verbose=verbose)
    self.auto_ob = None
    self.record_counter = 0
    self.mote_lists = mote_lists
    self.mote_observe_lists = mote_observe_lists
    self.autoOb_callback = autoOb_callback
    self.object_callback = object_callback
    self.signal = True
    self.countDown = countDown
    return

  def run(self):
    log.info("Starting auto observing nodes.")
    print("")
    if self.countDown is None:
      self.countDown = 60
    t = threading.Timer(int(self.countDown), self.freshBR)
    t.start()
    while self.signal:
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

      time.sleep(int(self.countDown)) # sleep 1mins.
      log.info("Observe ALL Done.")

      self.mote_lists = self.autoOb_callback(self.mote_observe_lists, False)

      for node in self.mote_observe_lists:
        print str(node.getName())+" -> Counter Ob : "+str(node.getCountOb())+", Counter Ck : "+str(node.getCountCk())
        if (node.getCountOb() - node.getCountCk()) > 2: # threshold number.
          node.saveCountCk(node.getCountOb()) # record fresh count number.
        else:
          node.stop()
          self.mote_observe_lists.remove(node)

      # except :
      #   log.info("Do not found moteAddress text.")
    t.cancel()
    return

  def stop(self):
    log.info("Stoping auto observing nodes.")
    self.signal = False
    return

  def freshBR(self):
    self.autoOb_callback(self.mote_observe_lists, True)