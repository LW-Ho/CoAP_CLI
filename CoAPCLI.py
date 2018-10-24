import logging.config
import os
from cmd import Cmd
from GetMotes import getAllMotes
import RestCoAP
from CoAPObserve import CoAPObserve

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
  #self.stdout.write("Would you want access mysql DB ? ")
  
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
    self.doc_header = 'Commands: \ngetallmotes \nlist \npost \npostall \nobserve \nobserveall \nobservelist \ndelete \ntest \nquit'
    self.prompt = '>'
    self.intro = '\nCoAP Command Line Tool, Welcome to use it!'

    self.mote_lists = []
    self.mote_observe_lists = []

  def do_getallmotes(self, arg):
    if not arg:
      self.stdout.write("Please provide Border router's IP address.\n")
      return
        
    try:
      self.stdout.write("Current Motes List : \n")
      self.mote_lists = getAllMotes(arg) # get motes from border router website.
      self.stdout.write("====== End of List =======\n")
    except:
      self.stdout.write("Error from getallmotes.\n")

  def do_list(self, arg):
    try:
      self.stdout.write("Current Motes List : \n")
      for index in range(0,len(self.mote_lists)):
        self.stdout.write("%d : %s\n" %(index+1, self.mote_lists[index]))
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
      print "get %.2f seconds... " %(pst)
      #print "Successful delivery."
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
      #print "get %.2f seconds... " %(pst)
      #print "Successful delivery."
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
      coapObserve.start()
      self.mote_observe_lists.append(coapObserve)
        #restCoAP.startObserve(node, resource)
      #print "Successful delivery."
    except:
      self.stdout.write("Error from observe.\n")
  
  def do_observeall(self, arg):
    if len(self.mote_lists) == 0:
      self.stdout.write("Please run getallmotes command.\n")
      return
    
    try :
      for line in self.mote_lists:
        coapObserve = CoAPObserve(node=line, resource="g/bcollect", object_callback=object_callback)
        coapObserve.printName()
        coapObserve.start()
        self.mote_observe_lists.append(coapObserve)
      self.stdout.write("Observe ALL Done.\n")
                
    except :
      self.stdout.write("Do not found moteAddress text.\n")
      return

  
  def do_observelist(self, arg):
    self.stdout.write("Current Observing Mote of Numbers: %d \n" %(len(self.mote_observe_lists)))
    if len(self.mote_observe_lists) != 0:
      for index in self.mote_observe_lists:
        index.printName()

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
        # else:
        #   self.stdout.write("Not found the mote, please check it out again.\n")

  def do_quit(self, arg):
    log.info("Stopping CoAPCLI...")

    while len(self.mote_observe_lists) != 0:
      for index in self.mote_observe_lists:
        log.info("Closing {0}!".format(index.getName()))
        self.mote_observe_lists.remove(index)
        index.stop()
    
    return True
      
        
if __name__=="__main__":
  optional_mysqlDB()
  collect_cli = CoAPCLI()
  collect_cli.cmdloop()