#!/usr/bin/python3
# -*- coding: utf-8; indent-tabs-mode: nil -*-
# http://daringfireball.net/projects/markdown/syntax
import urllib
import urllib.request
import urllib.parse  
import re
import mwparserfromhell
from urllib.error import *

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

outdir = "raw/"

class book:
     def __init__(self, name, url):
         self.url = url
         self.name = name
         

books = []
#tora
books.append(book("bereshit","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%AA%D7%95%D7%A8%D7%94_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%91%D7%A8%D7%90%D7%A9%D7%99%D7%AA"))
books.append(book("shmut","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%AA%D7%95%D7%A8%D7%94_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%A9%D7%9E%D7%95%D7%AA"))
books.append(book("vaikra","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%AA%D7%95%D7%A8%D7%94_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%95%D7%99%D7%A7%D7%A8%D7%90"))
books.append(book("bmidbar","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%AA%D7%95%D7%A8%D7%94_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%91%D7%9E%D7%93%D7%91%D7%A8"))
books.append(book("dvarim","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%AA%D7%95%D7%A8%D7%94_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%93%D7%91%D7%A8%D7%99%D7%9D"))

#neviim rishunum
books.append(book("yeushua","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%99%D7%94%D7%95%D7%A9%D7%A2/%D7%A9%D7%9C%D7%9D"))
books.append(book("shoftim","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%A9%D7%95%D7%A4%D7%98%D7%99%D7%9D/%D7%A9%D7%9C%D7%9D"))
books.append(book("shmuel","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%A9%D7%9E%D7%95%D7%90%D7%9C/%D7%A9%D7%9C%D7%9D"))
books.append(book("mlachim","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%9E%D7%9C%D7%9B%D7%99%D7%9D/%D7%A9%D7%9C%D7%9D"))

# neviim achronim
books.append(book("ishaia","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%99%D7%A9%D7%A2%D7%99%D7%94%D7%95/%D7%A9%D7%9C%D7%9D"))
books.append(book("irmia","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%99%D7%A8%D7%9E%D7%99%D7%94%D7%95/%D7%A9%D7%9C%D7%9D"))
books.append(book("ichezkel","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%99%D7%97%D7%96%D7%A7%D7%90%D7%9C/%D7%A9%D7%9C%D7%9D"))
books.append(book("treiasar","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%AA%D7%A8%D7%99_%D7%A2%D7%A9%D7%A8/%D7%A9%D7%9C%D7%9D"))

# emet
books.append(book("tehilim","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%AA%D7%94%D7%9C%D7%99%D7%9D/%D7%A1%D7%A4%D7%A8_%D7%A8%D7%90%D7%A9%D7%95%D7%9F"))
books.append(book("mishlei","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%9E%D7%A9%D7%9C%D7%99/%D7%A9%D7%9C%D7%9D"))
books.append(book("iyuv","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%90%D7%99%D7%95%D7%91/%D7%A9%D7%9C%D7%9D"))

# megilut
books.append(book("shir","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%9E%D7%92%D7%99%D7%9C%D7%AA_%D7%A9%D7%99%D7%A8_%D7%94%D7%A9%D7%99%D7%A8%D7%99%D7%9D/%D7%A9%D7%9C%D7%9D"))
books.append(book("root","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%9E%D7%92%D7%99%D7%9C%D7%AA_%D7%A8%D7%95%D7%AA/%D7%A9%D7%9C%D7%9D"))
books.append(book("icha","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%9E%D7%92%D7%99%D7%9C%D7%AA_%D7%90%D7%99%D7%9B%D7%94/%D7%A9%D7%9C%D7%9D"))
books.append(book("kohelet","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%9E%D7%92%D7%99%D7%9C%D7%AA_%D7%A7%D7%94%D7%9C%D7%AA/%D7%A9%D7%9C%D7%9D"))
books.append(book("ester","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%9E%D7%92%D7%99%D7%9C%D7%AA_%D7%90%D7%A1%D7%AA%D7%A8/%D7%A9%D7%9C%D7%9D"))

# #rest
books.append(book("daniel","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%93%D7%A0%D7%99%D7%90%D7%9C/%D7%A9%D7%9C%D7%9D"))
books.append(book("ezra","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%A2%D7%96%D7%A8%D7%90/%D7%A9%D7%9C%D7%9D"))
books.append(book("divrei","http://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/%D7%A0%D7%91%D7%99%D7%90%D7%99%D7%9D_%D7%95%D7%9B%D7%AA%D7%95%D7%91%D7%99%D7%9D_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94/%D7%A1%D7%A4%D7%A8_%D7%93%D7%91%D7%A8%D7%99_%D7%94%D7%99%D7%9E%D7%99%D7%9D/%D7%A9%D7%9C%D7%9D"))

def clearNode(text):
    tmp = text
    tmp = re.sub('\n', '', tmp)
    tmp = tmp.rstrip()
    tmp = re.sub('<.*?>', '', tmp)

    return tmp
def printbook(name, text):
    with open (outdir+name+'.raw', 'a') as f: f.write(text)

for b in books:
    text = opener.open(b.url+"?action=raw").read().decode("UTF-8")
    wiki = mwparserfromhell.parse(text)

    print(b.name)
    for node in wiki.nodes:
        node=clearNode(str(node))

        if re.match('{{תבנית:משתמש:Dovi/טעמי המקרא-סוף}}', node):
            break
        if re.match('{{\#קטע:', node):
            node = re.sub("{{\#קטע:(.*)\|.*}}","\g<1>",node)
            url = "http://he.wikisource.org/wiki/"+urllib.parse.quote(node)+"?action=raw"
            try:
                 tmp = opener.open(url).read().decode("UTF-8")
            except (HTTPError, URLError) as error:
                 print('Data of %s not retrieved because %s\nURL: %s', b.name, error, url)
            printbook(b.name, tmp)
