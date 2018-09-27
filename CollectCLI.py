import os
from cmd import Cmd
from getMotes import getmotes
from restCoAP import coap

class CollectCLI(Cmd):
  def __init__(self):
    log.info("Starting CollectCLI")

    Cmd.__init__(self)
    self.doc_header = 'Commands: \ngetallmotes \nget \ngetall'
    self.prompt = '>'
    self.intro = '\nCollectCLI, Welcome!'

    self.mote_lists = []
  
  def do_getallmotes(self, arg):
    if not arg:
      self.stdout.write("Please provide Border router's mac address.\n")
      return
    mote_lists = getmotes(arg) # get motes from border router website.
    self.stdout.write("====== End of List =======\n")

  def do_get(self, arg):
    if not arg:
      self.stdout.write("Please provide node's mac address.\n")
      return
    args = arg.split(' ')
    node = args[0]
    resource = args[1]

    for index in range(0,len(self.mote_lists)):
      if self.mote_lists[index] == node:
        if len(args) < 3: # if no query
          coap.getToNode(node,resource)
        else if len(agrs) > 4:
          self.stdout.write("Most too arguments, Please check it.\n")
          return
        else:
          query = args[2]
          coap.getQueryToNode(node,resource,query)
      else:
        self.stdout.write("Please check your typing mac address.\n")
        
if __name__=="__main__":
  collect_cli = CollectCLI()
  collect_cli.cmdloop()