import os
from cmd import Cmd
from getMotes import getAllMotes
import restCoAP

class CollectCLI(Cmd):
  def __init__(self):

    Cmd.__init__(self)
    self.doc_header = 'Commands: \ngetallmotes \nget \ngetall '
    self.prompt = '>'
    self.intro = '\nCollectCLI, Welcome!'

    self.mote_lists = []
  
  def do_getallmotes(self, arg):
    if not arg:
      self.stdout.write("Please provide Border router's mac address.\n")
      return
    mote_lists = getAllMotes(arg) # get motes from border router website.
    self.stdout.write("====== End of List =======\n")

  def do_get(self, arg):
    if not arg:
      self.stdout.write("Please provide node's mac address.\n")
      return

    args = arg.split(' ')
    if len(args) == 1:
      self.stdout.write("Need to typing resource.\n")
    else:
      node = args[0]
      resource = args[1]

    for index in range(0,len(self.mote_lists)):
      if self.mote_lists[index] == node:
        if len(args) == 2: # if no query
          restCoAP.getToNode(node,resource)
        elif len(agrs) == 3:
          query = args[2]
          restCoAP.getQueryToNode(node,resource,query)
        else:
          self.stdout.write("Most too arguments, Please check it.\n")
          return
      else:
        self.stdout.write("Please check your typing mac address.\n")
    

        
if __name__=="__main__":
  collect_cli = CollectCLI()
  collect_cli.cmdloop()