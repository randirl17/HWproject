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
import HWhtml
import string

def urlget(url,endfile):
#pull html from website and save as local file
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
#for stripping html tags from sections of txt file
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
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def Jap(file):
#This website updates regularly, so the 1st post under the "Homework" header is the relevant info.
  soup=BeautifulSoup(open(file),"lxml")
  column=soup.find_all(class_='sites-layout-tile sites-tile-name-content-1') #find general section with HW
  HWmatch=re.findall(r'Homework[\s\S]+',str(column[0]))
  match=re.findall(r'">([-\w\d\s,/]+)</font>',str(HWmatch[0]))
  return match
  
def Math(file):
#This website updates regularly, with the most recent announcement containing any HW updates.
  soup=BeautifulSoup(open(file),"lxml")
  title=soup.find(class_="announcement").h4.string
  a=soup.find(class_="announcement").div.contents
  dicta={}
  stripped = strip_tags(str(a))
  dicta['title']=title
  dicta['HW']=stripped
  return dicta
  
def Math2(file,date):
#This website contains a calendar in html table form of all the HW assignments for the month.
#Search table by date: 12/11 (B) etc.
  soup=BeautifulSoup(open(file),"lxml")
  table=list(soup.tbody.tr.td.div.children)
  today = date.strftime("%m/%d")+r'\n'
  if today not in str(table[2]):
    today = '2/22'
  today_ind = str(table[2]).index(today)
  tomor = date + dt.timedelta(days=1)
  tomorrow = tomor.strftime("%m/%d") + r'\n'
  if tomorrow not in str(table[2]):
    tomorrow = '2/23'
  tomor_ind = str(table[2]).index(tomorrow)
  chunk = str(table[2])[today_ind:tomor_ind]  #cuts out chunk of table with today's assignment+html
  actual = strip_tags(chunk)  #need to parse text out of html tags
  justtext = []
  for piece in actual:
    if not piece.startswith("\\"):
      noreturn = piece.replace(r'\n','')
      justtext.append(noreturn)  
  return justtext

def Sci(file,date):
#This website has a list of all HW assignments for the month.  Search bold headers for date:  Dec 13/14 etc
#Since this is B day, it's always listed 2nd.
#today 11, yest 10, 1b4 = 9, 2b4 = 8 
  soup = BeautifulSoup(open(file),"lxml")
  HW = {}
  month = date.strftime('%b')
  today = month + ' ' + date.strftime("%d").lstrip('0')
  yest = date + dt.timedelta(days=-1)
  yester = month + ' ' + yest.strftime('%d').lstrip('0') + '/' + date.strftime("%d").lstrip('0')  #this would be current
  dayb4 = date + dt.timedelta(days=-2)  #over weekends, may need to go back 3 days to get match
  daybefore = month + ' ' + dayb4.strftime('%d').lstrip('0') + '/' + yest.strftime('%d').lstrip('0')
  twodays = date + dt.timedelta(days=-3)
  twobefore = month + ' ' + twodays.strftime('%d').lstrip('0') + '/' + dayb4.strftime('%d').lstrip('0')
  threedays = date + dt.timedelta(days=-4)
  threebefore = month + ' ' + threedays.strftime('%d').lstrip('0') + '/' + twodays.strftime('%d').lstrip('0')
  print(today, yester, daybefore, twobefore, threebefore)
  title = today 
  for line in soup('b'):
    if yester in str(line) or daybefore in str(line) or twobefore in str(line) or threebefore in str(line):
      title = line.next_element
      assignment = line.next_element.next_element.next_element
  if title == today:  assignment = "No assignment found for today's date: " + str(today) 
  HW[title] = assignment
  return HW

def Hist(file,date):

  return


def HWscript(filename):
  dirname = './sitefiles'
  if not os.path.exists(dirname):  os.mkdir(dirname)
  date = dt.datetime.today() 
#  date = dt.datetime.today() - dt.timedelta(days=17)
  f = open(filename,'r') #open and read sites.txt list, formatted as subj: url
  for line in f:
    urlparts = line.split(":")
    classfile = urlparts[0].replace(' ','') + '.txt'
    site = urlparts[2]
    link = urlparts[1] + ":" + site[:-1]
    dest_name = os.path.join(dirname,classfile)
    urlget(link,dest_name)  #write html from web to txt files
    if "Jap" in urlparts[0]:  JapHW = Jap(dest_name)
    if "Math" == urlparts[0]:  MathHW = Math(dest_name)
    if "Sci" in urlparts[0]:  SciHW = Sci(dest_name,date)
    if "Math2" == urlparts[0]:  Math2HW = {'mathcal':  ''}#Math2(dest_name,date)
  f.close()
  HWhtml.makehtml(date, JapHW, MathHW, Math2HW, SciHW, 'HWpost.html')
  
#  print()
#  print("Japanese")
#  for Jitems in JapHW:  print(Jitems)
#  print()
#  print("Math")
#  print(MathHW['title'])
#  for Mitems in MathHW['HW']:  print(Mitems)
#  print()
#  print("Math part 2")
#  for M2items in Math2HW:  print(M2items)
#  print()
#  print("Science")
#  for key in SciHW:
#    print(key)
#    print(SciHW[key])
  return



def main():
  args = sys.argv[1:]

  if not args:
    print('usage: ./HWpull.py file')
    sys.exit(1)

  HWscript(args[0])
    

if __name__ == '__main__':
  main()
