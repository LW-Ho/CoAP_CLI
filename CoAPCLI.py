import os
from cmd import Cmd
from getMotes import getAllMotes
import restCoAP
from coap_observe import StartObserve

class CoAPCLI(Cmd):
  def __init__(self):

    Cmd.__init__(self)
    self.doc_header = 'Commands: \ngetallmotes \nlist \npost \nobserve \nobservelist \ndelete \nquit'
    self.prompt = '>'
    self.intro = '\nCollectCLI, Welcome!'

    self.mote_lists = []
    self.mote_observe_lists = []

  def do_getallmotes(self, arg):
    if not arg:
      self.stdout.write("Please provide Border router's mac address.\n")
      return
    try:
      self.mote_lists = getAllMotes(arg) # get motes from border router website.
      self.stdout.write("====== End of List =======\n")
    except:
      self.stdout.write("Error from getallmotes.\n")

  def do_list(self, arg):
    for index in range(0,len(self.mote_lists)):
      print "%d : %s" %(index+1, self.mote_lists[index])

  def do_post(self, arg):
    if not arg:
      self.stdout.write("Please provide node's mac address.\n")
      return

    args = arg.split(' ')

    try:
      node = args[0]
      resource = args[1]
      query = args[2]
      restCoAP.postQueryToNode(node, resource, query)
      self.stdout.write("Successful delivery.\n")
    except:
      self.stdout.write("Error from get.\n")
     
  def do_postall(self, arg):
    if not arg:
      self.stdout.write("Please provide arguments\n")
      return
    
    args = arg.split(' ')
    
    try:
      resource = args[0]
      query = args[1]
      restCoAP.postToAllNode(mote_lists, resource, query)
      self.stdout.write("Successful delivery.\n")
    except:
      self.stdout.write("Error from getall.\n")

  def do_observe(self, arg):
    if not arg:
      self.stdout.write("Please provide node's mac address.\n")
      return

    args = arg.split(' ')
    try:
      node = args[0]
      resource = args[1]
      coapObserve = StartObserve(node=node, resource=resource)
      coapObserve.getName()
      coapObserve.start()
      self.mote_observe_lists.append(coapObserve)
        #restCoAP.startObserve(node, resource)
      self.stdout.write("Successful delivery.\n")
    except:
      self.stdout.write("Error from observe.\n")
  
  def do_observelist(self, arg):
    if len(self.mote_observe_lists) != 0:
      print "Testing OB List ... "
      print self.mote_observe_lists
      for index in self.mote_observe_lists:
        print "mote of list : "+str(index.getName())
        index.getName()
        print "end of list ..."

  def do_delete(self, arg):
    if not arg:
      self.stdout.write("Please provide node's mac address.\n")
      return

    print "Testing delete ... "
    print self.mote_observe_lists

    if len(self.mote_observe_lists) != 0:
      for index in self.mote_observe_lists:
        temp = index.getName()
        print "Hi !"
        print temp
        print "Hello ~ "
        print "mote : "+str(index.getName())
        print "arg : "+str(arg)
        print "Done."
        if index.getName() == arg:
          index.stop()
          self.mote_observe_lists.remove(index)
          print "Delete got %s" %(str(arg))
        else:
          self.stdout.write("Not found the mote, please check it out again.\n")

  def do_quit(self, arg):
    return True
      
        
if __name__=="__main__":
  collect_cli = CoAPCLI()
  collect_cli.cmdloop()