try:
    from HTMLParser import HTMLParser
    from urllib2 import urlopen
except ImportError:
    from html.parser import HTMLParser
    from urllib.request import urlopen
import sys

class PrintLinks(HTMLParser):
    def handle_starttag(self,tag,attrs):
        #if tag == 'a':
           # for name,value in attrs:
               # if name == 'href': print("Links-on-this-site:  ",value)
        if tag == 'img':
            for name,value in attrs:
                if name == 'alt':print("info:  ",value)
                if name == 'src':print("url-of-photo:  ",value)
        if tag == 'div':
            for name,value in attrs:
                if name == 'data-tutor-info':print("zip-codes:  ",value[30:-1].strip()
)

p = PrintLinks()
u = urlopen(sys.argv[1])
data = u.read()
charset = u.info().getparam('charset')
p.feed(data.decode(charset))
p.close()
