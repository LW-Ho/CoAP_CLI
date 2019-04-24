from bs4 import BeautifulSoup
import requests
import string
import TopologyTable


def getAllMotes(host):
  motes_List = []
  # parent_table = []
  topology_table = []
  child = ''
  parent = ''
    # save mote's address to file, will take it observe to all motes.
    #fo = open("../motesAddress","w")

  hostStr = "http://["+host+"]/"
  try:
    res = requests.get(hostStr) # get website data
  except:
    print "Failed to get border-router link...  \nPlease wait a minutes, then try again."
  # return motes_List

  soup = BeautifulSoup(res.text, 'html.parser')
  mote_tags = soup.find_all('li', class_="link") # find <li> html tag bind class name.
  for tag in mote_tags:
    #print tag
    motesStr = tag.string
    motesStr = motesStr.encode('utf-8') # encode unicode
    motesStr = motesStr.replace(')','')
    #print motesStr
    motesStr = motesStr.split()
    #print motesStr

    for index in range(0, len(motesStr), 4):
        #fo.write("add "+motesStr[index]+" bcollect\n")
        #fo.write(motesStr[index]+"\n")
      temp = []
      for parent_index in range(2, len(motesStr), 4):
        parent = motesStr[parent_index]
        temp.append(parent)

      child = motesStr[index]
      temp.append(child)
      topology_table.append(temp)
      motes_List.append(motesStr[index])
      #print motesStr[index]

  TopologyTable.set_table(host, topology_table)
    #fo.close()
  return motes_List # return mote lists
#getAllMotes Done.