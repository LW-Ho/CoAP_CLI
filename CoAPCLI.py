import os
from cmd import Cmd
from getMotes import getAllMotes
import restCoAP
from coap_observe import StartObserve

class CoAPCLI(Cmd):
  def __init__(self):

    Cmd.__init__(self)
    self.doc_header = 'Commands: \ngetallmotes \nlist \npost \npostall \nobserve \nobservelist \ndelete \nquit'
    self.prompt = '>'
    self.intro = '\nCoAP Command Line Tool, Welcome to use it!'

    self.mote_lists = []
    self.mote_observe_lists = []

  def do_getallmotes(self, arg):
    if not arg:
      print "Please provide Border router's IP address."
      return
    try:
      self.mote_lists = getAllMotes(arg) # get motes from border router website.
      print "====== End of List ======="
    except:
      print "Error from getallmotes."

  def do_list(self, arg):
    for index in range(0,len(self.mote_lists)):
      print "%d : %s" %(index+1, self.mote_lists[index])

  def do_post(self, arg):
    if not arg:
      print "Please provide node's IP address."
      return

    args = arg.split(' ')

    try:
      node = args[0]
      resource = args[1]
      query = args[2]
      restCoAP.postQueryToNode(node, resource, query)
      #print "Successful delivery."
    except:
      print "Error from post."
     
  def do_postall(self, arg):
    if not arg:
      print "Please provide arguments"
      return
    
    args = arg.split(' ')
    
    try:
      resource = args[0]
      query = args[1]
      restCoAP.postToAllNode(self.mote_lists, resource, query)
      #print "Successful delivery."
    except:
      print "Error from postall."

  def do_observe(self, arg):
    if not arg:
      print "Please provide node's IP address."
      return

    args = arg.split(' ')
    try:
      node = args[0]
      resource = args[1]
      coapObserve = StartObserve(node=node, resource=resource)
      coapObserve.printName()
      coapObserve.start()
      self.mote_observe_lists.append(coapObserve)
        #restCoAP.startObserve(node, resource)
      #print "Successful delivery."
    except:
      print "Error from observe."
  
  def do_observelist(self, arg):
    if len(self.mote_observe_lists) != 0:
      for index in self.mote_observe_lists:
        index.printName()

  def do_delete(self, arg):
    if not arg:
      print "Please provide node's IP address." 
      return

    if len(self.mote_observe_lists) != 0:
      for index in self.mote_observe_lists:
        if index.getName() == arg:
          index.stop()
          self.mote_observe_lists.remove(index)
          print "Delete got %s" %(str(arg))
        else:
          print "Not found the mote, please check it out again."

  def do_quit(self, arg):
    return True
      
        
if __name__=="__main__":
  collect_cli = CoAPCLI()
  collect_cli.cmdloop()