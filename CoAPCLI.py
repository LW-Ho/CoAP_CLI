import logging.config
import os
import sys
from cmd import Cmd
from GetMotes import getAllMotes
import RestCoAP
from CoAPObserve import CoAPObserve
from AutoOb import AutoOb

logging.config.fileConfig(os.path.join('logging.conf'))
log = logging.getLogger("root")

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('config.cfg')

# if false, data can't saving to db.
flag_DB = None

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
engine = create_engine('mysql+mysqlconnector://{username}:{password}@{host}/{database}'.format(username=config.get('database', 'username'),
                                                                                               password=config.get('database', 'password'),
                                                                                               host=config.get('database', 'host'),
                                                                                               database=config.get('database', 'database'),
                                                                                               ), echo=False)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def object_callback(mote_data):
    try:
        #log.info("Got new object_callback")
        #log.debug(mote_data)

        if flag_DB :
          #log.info("Got new object_callback in flag_DB")
          session = Session()
          session.add(mote_data)
          session.commit()
    except:
        log.error("Got Error! You Need to started MySQL service.")
        import sys
        log.critical("Unexpected error:{0}".format(sys.exc_info()[0]))
        log.critical("Unexpected error:{0}".format(sys.exc_info()[1]))

def optional_mysqlDB():
  global flag_DB
  
  while flag_DB is None:
    db = raw_input("Would you want access data to MySQL DB ?(Y/N) ")

    if db == "Y" or db == "y" :
      print "You press Yes."
      flag_DB = True
    elif db == "N" or db =="n" :
      print "You press No."
      flag_DB = False
    else :
      print "Enter again."
      flag_DB = None

class CoAPCLI(Cmd):
  def __init__(self):
    log.info("Starting CoAPCLI...")

    Cmd.__init__(self)
    self.doc_header = 'Commands: \ngetallmotes \nlist \npost \npostall \nobserve \nobserveall \nobservelist \ndelete \nauto \nquit'
    self.prompt = '>'
    self.intro = '\nCoAP Command Line Tool, Welcome to use it!'

    self.mote_lists = []
    self.mote_observe_lists = []
    self.autoObserve = None # save autoOb class
    self.border_router_Addr = ""

  def do_getallmotes(self, arg):
    if not arg:
      self.stdout.write("Please provide Border router's IP address.\n")
      return
    self.border_router_Addr = arg
    try:
      self.stdout.write("Current Motes List : \n")
      self.mote_lists = getAllMotes(self.border_router_Addr) # get motes from border router website.
      self.stdout.write("====== End of List =======\n")
    except:
      self.stdout.write("Error from getallmotes.\n")

  def do_list(self, arg):
    try:
      self.stdout.write("Current Motes List : \n")
      for index in range(0,len(self.mote_lists)):
        self.stdout.write("%2d : %s\n" %(index+1, self.mote_lists[index]))
      self.stdout.write("====== End of List =======\n")
    except:
      self.stdout.write("Error from list.\n")

  def do_post(self, arg):
    if not arg:
      self.stdout.write("Please provide node's IP address.\n")
      return

    args = arg.split(' ')
  
    try:
      node = args[0]
      resource = args[1]
      query = args[2]
      pst = RestCoAP.postQueryToNode(node, resource, query)
    except:
      self.stdout.write("Error from post.\n")
     
  def do_postall(self, arg):
    if not arg:
      self.stdout.write("Please provide arguments\n")
      return
    
    args = arg.split(' ')
    
    try:
      resource = args[0]
      query = args[1]
      RestCoAP.postToAllNode(self.mote_lists, resource, query)
    except:
      self.stdout.write("Error from postall.\n")

  def do_observe(self, arg):
    if not arg:
      self.stdout.write("Please provide node's IP address.\n")
      return

    args = arg.split(' ')
    try:
      node = args[0]
      resource = "g/"+str(args[1])
      coapObserve = CoAPObserve(node=node, resource=resource, object_callback=object_callback)
      coapObserve.printName()
      coapObserve.setDaemon(True)
      coapObserve.start()
      self.mote_observe_lists.append(coapObserve)
    except:
      self.stdout.write("Error from observe.\n")
  
  def do_observeall(self, arg):
    if len(self.mote_lists) == 0:
      self.stdout.write("Please run getallmotes command.\n")
      return
    self.do_observelist("arg") # refresh observe_list.
    s1 = set(self.mote_lists)
    temp = []

    for obnode in self.mote_observe_lists: # to change element type, then save to oher list. (CoAP to string)
      temp.append(obnode.getName())
    s2 = set(temp)

    result = list(s1.difference(s2)) # compare list,we can know that is not observing.
    
    try :
      for node in result:
        coapObserve = CoAPObserve(node=node, resource="g/bcollect", object_callback=object_callback)
        coapObserve.printName()
        coapObserve.setDaemon(True)
        coapObserve.start()
        self.mote_observe_lists.append(coapObserve)

      self.stdout.write("Observe ALL Done.\n")
                
    except :
      self.stdout.write("Do not found moteAddress text.\n")
      return

  def do_observelist(self, arg):
    if len(self.mote_observe_lists) != 0:
      for index in self.mote_observe_lists:
        if index.getFlag() is False:
          if not arg:
            index.printName()
          else:
            continue
        else:
          self.mote_observe_lists.remove(index)

    self.stdout.write("Current Observing Mote of Numbers: %d \n" %(len(self.mote_observe_lists)))

  def do_delete(self, arg):
    if not arg:
      self.stdout.write("Please provide node's IP address.\n")
      return

    if len(self.mote_observe_lists) != 0:
      for index in self.mote_observe_lists:
        if index.getName() == arg:
          index.stop()
          self.mote_observe_lists.remove(index)
          self.stdout.write("Delete got %s\n" %(str(arg)))

  def do_auto(self, arg):
    args = arg.split(' ')

    if args[0] == "start":
      if self.autoObserve is None and len(self.mote_lists) != 0 :
        if len(args) == 2:
          self.autoObserve = AutoOb(mote_lists=self.mote_lists, mote_observe_lists=self.mote_observe_lists, countDown=args[1], autoOb_callback=self.autoOb_callback, object_callback=object_callback)
        else:
          self.autoObserve = AutoOb(mote_lists=self.mote_lists, mote_observe_lists=self.mote_observe_lists, autoOb_callback=self.autoOb_callback, object_callback=object_callback)
        self.autoObserve.setDaemon(True)
        self.autoObserve.start()
      elif len(self.mote_lists) == 0:
        self.stdout.write("Please run getallmotes command.\n")
        return
      else:
        self.stdout.write("Running... You can't run again.\n")
        self.stdout.write("You must stop before you can start again.\n")
    elif args[0] == "stop" and self.autoObserve is not None:
      self.autoObserve.stop()
    else:
      self.stdout.write("Need type auto start or auto stop.\n")
      return

  def autoOb_callback(self, mote_observe_Lists, refreshTopology):
    # using callback function to maintain mote_lists and mote_observe_lists.
    self.mote_observe_lists = mote_observe_Lists

    if refreshTopology is True :
      self.mote_lists = getAllMotes(self.border_router_Addr)
      self.stdout.write("Updating Topology...\n")
    else:
      return self.mote_lists
    
  def do_quit(self, arg):
    log.info("Stopping CoAPCLI...")

    while len(self.mote_observe_lists) != 0:
      for index in self.mote_observe_lists:
        log.info("Closing {0}!".format(index.getName()))
        self.mote_observe_lists.remove(index)
        index.stop()
        index.join() # testing, join to main thread, will be release it.
    sys.exit(1)
    
      
        
if __name__=="__main__":
  optional_mysqlDB()
  collect_cli = CoAPCLI()
  collect_cli.cmdloop()