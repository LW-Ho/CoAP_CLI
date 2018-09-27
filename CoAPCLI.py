import os
from cmd import Cmd
from getMotes import getAllMotes
import restCoAP

class CoAPCLI(Cmd):
  def __init__(self):

    Cmd.__init__(self)
    self.doc_header = 'Commands: \ngetallmotes \nget \ngetall \nobserve \nobserveall'
    self.prompt = '>'
    self.intro = '\nCollectCLI, Welcome!'

    self.mote_lists = []
  
  def do_getallmotes(self, arg):
    if not arg:
      self.stdout.write("Please provide Border router's mac address.\n")
      return
    try:
      mote_lists = getAllMotes(arg) # get motes from border router website.
      self.stdout.write("====== End of List =======\n")
    except:
      self.stdout.write("Error from getallmotes.")

  def do_get(self, arg):
    if not arg:
      self.stdout.write("Please provide node's mac address.\n")
      return

    args = arg.split(' ')
    try:
      if len(args) < 2:
        self.stdout.write("Need to typing resource.\n")
        return
      else:
        node = args[0]
        resource = args[1]

      for index in range(0,len(self.mote_lists)):
        if self.mote_lists[index] == node:
          if len(agrs) == 3:
            query = args[2]
            restCoAP.getQueryToNode(node,resource,query)
          else:
            self.stdout.write("Most too arguments, Please check it.\n")
        else:
          self.stdout.write("Please check your typing mac address or query.\n")
    except:
      self.stdout.write("Error from get.")
  
  def do_gatall(self, arg):
    if not arg:
      self.stdout.write("Please provide node's mac address.\n")
      return
    
    args = arg.split(' ')
    try:
      if len(args) < 2:
        self.stdout.write("Need to typing resource.\n")
        return
      else:
        resource = args[0]
        query = args[1]

      restCoAP.getToAllNode(mote_lists, resource, query)
    except:
      self.stdout.write("Error from getall.")
    
  def do_observe(self, arg):
    if not arg:
      self.stdout.write("Please provide node's mac address.\n")
      return
    
    try:
      if len(args) < 2:
        self.stdout.write("Need to typing resource.\n")
        return
      else:
        node = args[0]
        resource = args[1]

      for index in range(0,len(self.mote_lists)):
        if self.mote_lists[index] == node:
          if len(agrs) < 3:
            restCoAP.startObserve(node,resource)
          else:
            self.stdout.write("Most too arguments, Please check it.\n")
        else:
          self.stdout.write("Please check your typing mac address or query.\n")
    except:
      self.stdout.write("Error from get.")

      

        
if __name__=="__main__":
  collect_cli = CoAPCLI()
  collect_cli.cmdloop()