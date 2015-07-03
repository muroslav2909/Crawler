from urllib2 import urlopen
from HTMLParser import HTMLParser
import re
import csv
import urllib


def get_page_code(link, class1):
        u = urlopen(link)
        data = u.read()
        charset = u.info().getparam('charset')
        class1.feed(data.decode(charset))
        class1.close()


class GetCityLink(HTMLParser):

    mas_link_city = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name,value in attrs:
                if name == 'href':
                    self.mas_link_city.append(value.encode('utf-8'))
                    print "mas_link_city: ", value

class GetTutorLink(HTMLParser):

    all_links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name,value in attrs:
                if name == 'href':
                    part_of_link = 'universitytutor.com/tutors/'
                    if (re.search(part_of_link,value) != None) and ( (value in self.all_links) == False):
                        try:
                            self.all_links.append(value.encode('utf-8'))
                            print "all_link: ", value
                        except:
                            print "Oops!  Something is wrong"

class GetTutorsInfo(HTMLParser):

    mas_city = []
    mas_name = []
    mas_subject = []
    mas_post_zip = []
    mas_url_photo = []
    mas_country = []
    mas_joined = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for name,value in attrs:
                if name == 'src':
                    self.mas_url_photo.append(value)
                    print("url-of-photo:  ", value)
        if tag == 'div':
            for name, value in attrs:
                if name == 'data-tutor-info':
                    paragraph_left = 27
                    paragraph_right = -1
                    zip_code = value[paragraph_left:paragraph_right].encode('utf-8')
                    if zip_code.isdigit():
                        print "zip_code:  ",zip_code
                        self.mas_post_zip.append(zip_code)
                    else:
                        self.mas_post_zip.append('None')
        if tag == 'img':
            for name,value in attrs:
                if name == 'alt':
                    s1 = value.split()
                    country = ''
                    for n, w in enumerate(s1):
                        if w == 'a':
                            city = s1[n+1]
                            if ',' in city:
                                paragraph_left1 = 0
                                paragraph_right1 = -1
                                city = city[paragraph_left1:paragraph_right1]
                                country = s1[n+2]
                                print "country:  ", country
                            print "city:  ", city
                        if w == 'is':
                            name = s1[n-1]
                            if '.' in name:
                             name = name[paragraph_left1:paragraph_right1]
                            print "name:  ", name
                    self.mas_city.append(city)
                    self.mas_name.append(name)
                    self.mas_country.append(country)
        if tag == 'meta':
            for name, value in attrs:
                if (name == 'name') and (value == 'keywords'):
                    for name,value in attrs:
                        if name == 'content':
                            s1 = value.split()
                            for n, w in enumerate(s1):
                                if w == 'tutor,':
                                    z= 5
                                    subject = ''
                                    while z < len(s1):
                                        subject = subject + s1[n+z]
                                        z = z + 1
                                    print "subject:  ",subject
                                    self.mas_subject.append(subject)
def SearchText(link):
        infile = urllib.urlopen(link)
        lines = infile.readlines()
        for i in range(len(lines)):
            line = lines[i]
            if '<i class="fa fa-map-marker"></i' in line:
                without_space = lines[i+4].strip()
                print " date joined_before   : " + without_space
                name = without_space[10:]
                print " date joined   : " + name
                info.mas_joined.append(name)


def WriteToCSV():
    with open('universitytutor.csv', 'w') as csvfile:
        fieldnames = ['name', 'city', 'country', 'zip-code','url-of-profile', 'url-of-photo', 'subject']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        l = 0
        while l < len(m.all_links):
             try:
                writer.writerow({'name': info.mas_name[l], 'city': info.mas_city[l], 'country': "Indonezia",'zip-code': info.mas_post_zip[l], 'url-of-profile': m.all_links[l], 'url-of-photo': info.mas_url_photo[l], 'subject': info.mas_subject[l]})
                l = l+1
             except:
                break

mother_link = 'http://kuching.universitytutor.com/kuching_tutoring'

p = GetCityLink()
get_page_code(mother_link, p)

m = GetTutorLink()
i = 0
print 'len(p.mas_link_city)= ', len(p.mas_link_city)
while i < len(p.mas_link_city):
    try:
     get_page_code(p.mas_link_city[i], m)
    except:
     print " problem url is (p) = ", p.mas_link_city[i]
    i = i + 1

info = GetTutorsInfo()
k = 0
print 'len(m.all_links)= ', len(m.all_links)
while k < len(m.all_links):
    get_page_code(m.all_links[k], info)
    SearchText(m.all_links[k])
    k = k + 1


WriteToCSV()
