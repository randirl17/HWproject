"""
Takes sites.txt list of websites, determines class name, downloads html and finds most recent assignment for each course.  Then writes these assignments to a single html file.
"""

import os
import re
import sys
import urllib.request
from bs4 import BeautifulSoup
import datetime as dt
from html.parser import HTMLParser

def urlget(url,endfile):
  try:
      ufile = urllib.request.urlopen(url)
      udict = dict(ufile.info())
      if 'text/html' in udict['Content-Type']:
        text=str(ufile.read())
        h=open(endfile,'w')
        h.write(text)
        h.close()
  except IOError:
    print('problem reading url:', url)

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return list(self.fed)

def strip_tags(html):
#    parser = HTMLParser()
#    html = parser.unescape(html)
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def Jap(file):
  soup=BeautifulSoup(open(file),"lxml")
  column=soup.find_all(class_='sites-layout-tile sites-tile-name-content-1') #find general section with HW
  HWmatch=re.findall(r'Homework[\s\S]+',str(column[0]))
  match=re.findall(r'">([-\w\d\s,/]+)</font>',str(HWmatch[0]))
  return match
  
def Math(file):
  soup=BeautifulSoup(open(file),"lxml")
  title=soup.find(class_="announcement").h4.string
  a=soup.find(class_="announcement").div.contents
  newa=[]
  dicta={}
  stripped = strip_tags(str(a))
  dicta['title']=title
  dicta['HW']=stripped
  return dicta
  
def Math2(file):
  soup=BeautifulSoup(open(file),"lxml")
  table=list(soup.tbody.tr.td.div.children)
  today = dt.datetime.today().strftime("%m/%d")+r'\n'
  today_ind = str(table[2]).index(today)
  tomor = dt.datetime.today() + dt.timedelta(days=1)
  tomorrow = tomor.strftime("%m/%d") + r'\n'
  tomor_ind = str(table[2]).index(tomorrow)
  chunk = str(table[2])[today_ind:tomor_ind]  #cuts out chunk of table with today's assignment+html
  actual = strip_tags(chunk)  #need to parse text out of html tags
  justtext = []
  for piece in actual:
    if not piece.startswith("\\"):
      noreturn = piece.replace(r'\n','')
      justtext.append(noreturn)  
  return justtext

def Sci(file):
  return

def HWscript(filename):
  dirname='./sitefiles'
  if not os.path.exists(dirname):  os.mkdir(dirname)
  f=open(filename,'r') #open and read sites.txt list
  for line in f:
    urlparts=line.split(":")
    classfile=urlparts[0].replace(' ','')+'.txt'
    site=urlparts[2]
    link=urlparts[1]+":"+site[:-1]
    dest_name=os.path.join(dirname,classfile)
    urlget(link,dest_name)  #write html to txt files
    if "Jap" in urlparts[0]:  JapHW=Jap(dest_name)
    if "Math" == urlparts[0]:  MathHW=Math(dest_name)
    if "Science" == urlparts[0]:  SciHW=''
    if "Math2" == urlparts[0]:  Math2HW=Math2(dest_name)
  f.close()

  print()
  print("Japanese")
  for Jitems in JapHW:  print(Jitems)
  print()
  print("Math")
  print(MathHW['title'])
  for Mitems in MathHW['HW']:  print(Mitems)
  print()
  print("Math part 2")
  for M2items in Math2HW:  print(M2items)
  print()
  print("Science")
  print(SciHW)
#  for Sitems in SciHW:  print(Sitems)
  



    
  return



def main():
    img_urls = HWscript(sys.argv[1])


if __name__ == '__main__':
  main()
