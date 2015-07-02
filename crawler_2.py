try:
    from HTMLParser import HTMLParser
    from urllib2 import urlopen
except ImportError:
    from html.parser import HTMLParser
    from urllib.request import urlopen
import sys
import re
import csv
import urllib
from string import maketrans

class SearchLinks(HTMLParser):

    masLink = []
    def handle_starttag(self,tag,attrs):
        if tag == 'a':
            for name,value in attrs:
               if name == 'href':
                    # for v in value:
                    m = 'universitytutor.com/tutors/'
                    if (re.search(m,value) != None):
                        if ( (value in self.masLink) == False):
                            self.masLink.append(value.encode('utf-8'))
                            print "Links-on-this-site:  ",value


class SearchInfo(HTMLParser):
    masCity = []
    masName = []
    masSubject = []
    masSubjectSplit = []
    masZip = []
    masPhoto = []
    def handle_starttag(self,tag1,attrs1):
        if tag1 == 'img':
            for name,value in attrs1:
                if name == 'alt':
                    s1 = value.split()
                    for n, w in enumerate(s1):
                        if w == 'a':
                            city = s1[n+1]
                            if ',' in city:
                             city = city[0:-1]
                            #print("city:  ",city)
                        if w == 'is':
                            name = s1[n-1]
                            if '.' in name:
                             name = name[0:-1]
                           # print("name:  ",name)
                    self.masCity.append(city)
                    self.masName.append(name)

                if name == 'src':
                    #print("url-of-photo:  ",value)
                    self.masPhoto.append(value)
        if tag1 == 'div':
            for name,value in attrs1:
                if name == 'data-tutor-info':
                    #print("zip-codes:  ",value[30:-1].strip())
                    self.masZip.append(value[30:-1].encode('utf-8'))
        if tag1 == 'meta':
            for name,value in attrs1:
                if name == 'content':
                    #table = maketrans('$%]/[', '')
                   # value.translate(table)
                    self.masSubject.append(value.encode('utf-8'))


lines = []
with open('city.txt') as f:
    lines = f.readlines()

i = 0
p = SearchLinks()
while i < len(lines):
    u = urlopen(lines[i])
    data = u.read()
    charset = u.info().getparam('charset')
    p.feed(data.decode(charset))
    p.close()
    i = i+1

m =  SearchInfo()
k=0
z = 0
text_subject = []
lines2 = []
while k < len(p.masLink):
    u = urlopen(p.masLink[k])
    data1 = u.read()
    charset = u.info().getparam('charset')
    m.feed(data1.decode(charset))

    print "masCity:  ",m.masCity[k]
    print "masName:  ",m.masName[k]

    #infile = urllib.urlopen(p.masLink[k])
    k = k+1
# for z in range(len(lines2)):
#     lines2= infile.readlines()
#     if '<meta name="keywords"' in lines[z]:
#          while z < len(p.masLink):
#             text_subject = lines2[z]
#             m.masSubject.append(text_subject.encode('utf-8'))
#     print "masSubject:  ",m.masSubject[z]
#     z = z+1
    m.close()



with open('names.csv', 'w') as csvfile:
    fieldnames = ['name', 'city', 'country', 'zip-code','url-of-profile', 'url-of-photo', 'subject']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    l = 0
    while l <  len(p.masLink):
        writer.writerow({'name': m.masName[l], 'city': m.masCity[l], 'country': "Indonezia",'zip-code': m.masZip[l], 'url-of-profile': p.masLink[l], 'url-of-photo': m.masPhoto[l], 'subject': m.masSubject[l]})
        l = l+1
