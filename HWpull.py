#program to pull HW info from various websites and consolidate that to a single webpage

import os
import re
import sys
import urllib

def urlget(url,endfile):
  try:
    ufile = urllib.urlopen(url)
    if ufile.info().gettype() == 'text/html':
        text=ufile.read()
        h=open(endfile,'w')
        h.write(text)
        h.close()
  except IOError:
    print 'problem reading url:', link

def Jap(file):
  j=open(file,'r')
  jtxt=j.readlines()
  j.close()
  for line in jtxt:
    if ">-Homework" in line:
        return line
  return

def HWscript(filename):
  dirname='./sitefiles'
  if not os.path.exists(dirname):  os.mkdir(dirname)
  f=open(filename,'r') #open and read sites.txt
  for line in f:
    urlparts=line.split(":")
    classfile=urlparts[0].replace(' ','')+'.txt'
    site=urlparts[2]
    link=urlparts[1]+":"+site[:-1]
    dest_name=os.path.join(dir,classfile)
    urlget(link,dest_name)  #write html to txt files
    if "Jap" in urlparts[0]:  JapHW=Jap(dest_name)
  f.close()
#  z=open('HWlist.txt','a')
  



    
  return



def main():
    img_urls = HWscript(sys.argv[1])


if __name__ == '__main__':
  main()
