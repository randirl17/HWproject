"""
blank html template
"""
import sys
import datetime as dt

def makehtml(hw1, hw2, hw3, hw4, name):
  date = dt.datetime.today() - dt.timedelta(days=10)
  prettydate = date.strftime('%B %d, %Y')
  with open(name,'w') as f:
      f.write('<html>')
      f.write('<title>')
      f.write("Homework Summary")
      f.write('</title>')
      f.write('<style>')
      f.write('.class {')
      f.write('      color: blue;')
      f.write('      font-weight: bold;')
      f.write('      font-family:  verdana;')
      f.write('}')
      f.write('</style>')
      f.write('<h1>')
      f.write(prettydate)
      f.write('</h1>')
      f.write('<h2>')
      f.write("A Day:")
      f.write('</h2>')
#      f.write('<h3 class="class">')
#      f.write('Math & the Arts')
#      f.write('</h3>')
      f.write('<h3 class="class">')
      f.write('History')
      f.write('</h3>')
      f.write('<p>')
      f.write('')
      f.write('</p>')
      f.write('<h3 class="class">')
      f.write('Japanese')
      f.write('</h3>')
      for Jitems in hw1:
          f.write('<p>')
          f.write(Jitems)
          f.write('</p>')
      f.write('<h3 class="class">')
      f.write('Math')
      f.write('</h3>')
      f.write('<p>')
      f.write(hw2['title'])
      f.write('</p>')
      for Mitems in hw2['HW']:
          f.write('<p>')
          f.write(Mitems)
          f.write('</p>')
      for M2items in hw3:
          f.write('<p>')
          f.write(M2items)
          f.write('</p>')
      f.write('<h2>')
      f.write("B Day:")
      f.write('</h2>')
#      f.write('<h3 class="class">')
#      f.write('Science Fiction')
#      f.write('</h3>')
      f.write('<h3 class="class">')
      f.write('Science')
      f.write('</h3>')
      for key in hw4:
          f.write('<p>')
          f.write(hw4[key])
          f.write('</p>')
      f.write('<h3 class="class">')
      f.write('English')
      f.write('</h3>')
      f.write('<p>')
      f.write('This site requires a login to access.')
      f.write('</p>')
#      f.write('<h3 class="class">')
#      f.write('P.E.')
#      f.write('</h3>')

      f.write('</html>')      
  f.close()
  return


def main():
     makehtml(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
  main()
