"""
Takes sites.txt list of websites, determines class name, downloads html and finds most recent assignment for each course.  Then writes these assignments to a single html file.
"""

import os
import re
import sys
import urllib.request
from bs4 import BeautifulSoup

def urlget(url,endfile):
  try:
      ufile = urllib.request.urlopen(url)
      print(ufile.info())
      if ufile.info() == 'text/html':
        text=ufile.read()
        h=open(endfile,'w')
        h.write(text)
        h.close()
  except IOError:
    print('problem reading url:', link)

def Jap(file):
  soup=BeautifulSoup(open(file))
  column=soup.find_all(class_='sites-layout-tile sites-tile-name-content-1') #find general section with HW
  HWmatch=re.findall(r'Homework[\s\S]+',str(column[0]))
  match=re.findall(r'">([-\w\d\s,/]+)</font>',str(HWmatch[0]))
  return match
  
def Math(file):
  soup=BeautifulSoup(open(file))
  title=soup.find(class_="announcement").h4.string
  a=soup.find(class_="announcement").div.contents
  newa=[]
  for i in range(len(a)):
    newa.append(str(a[i]).strip("</div>"))
  return title+str(newa)
  


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
    if "Math" in urlparts[0]:  MathHW=Math(dest_name)
  f.close()

  print(JapHW)
  print()
  print(MathHW)  



    
  return



def main():
    img_urls = HWscript(sys.argv[1])


if __name__ == '__main__':
  main()
