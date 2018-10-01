from bs4 import BeautifulSoup
import requests
import string



def getAllMotes(host):
  motes_List = []

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
    motes_List.append(motesStr[index])
    print motesStr[index]
  
  return motesStr # return mote lists

#getAllMotes Done.