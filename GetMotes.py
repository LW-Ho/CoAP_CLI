from bs4 import BeautifulSoup
import requests
import string

def getAllMotes(host):
  motes_List = []

  # save mote's address to file, will take it observe to all motes.
  fo = open("../motesAddress","w")

  hostStr = "http://["+host+"]/"
  res = requests.get(hostStr) # get website data

  soup = BeautifulSoup(res.text, 'html.parser')
  mote_tags = soup.find_all('pre') # find <pre> html tag
  for tag in mote_tags:
    tag
  motesStr = tag.string
  motesStr = motesStr.encode('utf-8') # encode unicode
  motesStr = motesStr.split()

  for index in range(0,len(motesStr),4):
    #fo.write("add "+motesStr[index]+" bcollect\n")
    fo.write(motesStr[index]+"\n")
    motes_List.append(motesStr[index])
    print motesStr[index]
  
  fo.close()
  return motes_List # return mote lists

#getAllMotes Done.