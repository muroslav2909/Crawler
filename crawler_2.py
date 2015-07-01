try:
    from HTMLParser import HTMLParser
    from urllib2 import urlopen
except ImportError:
    from html.parser import HTMLParser
    from urllib.request import urlopen
    import sys
    import re

class SearchLinks(HTMLParser):
  #  def validate(link):
     #  if link.find('universitytutor.com/tutors/'):
     #      with open("true_link.txt","w") as out:
#                 out.write(link)

    def handle_starttag(self,tag,attrs):
        if tag == 'a':
            for name,value in attrs:
               if name == 'href':
                    for v in value:
                         m = "universitytutor.com/tutors/"
                         if re.search(m,v) != None:
                            print("Links-on-this-site:  ",v)

class SearchInfo(HTMLParser):
    def handle_starttag(self,tag,attrs):
        if tag == 'img':
            for name,value in attrs:
                if name == 'alt':print("info:  ",value)
                if name == 'src':print("url-of-photo:  ",value)
        if tag == 'div':
            for name,value in attrs:
                if name == 'data-tutor-info':print("zip-codes:  ",value[30:-1].strip())


lines = []
with open('city.txt') as f:
    lines = f.readlines()
    print(lines)
i = 0


p = SearchLinks()
while i<20:
    u = urlopen(lines[0])
    data = u.read()
    charset = u.info().getparam('charset')
    p.feed(data.decode(charset))
    p.close()
    i = i+1
