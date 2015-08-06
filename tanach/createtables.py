#!/usr/bin/python3
# -*- coding: utf-8; indent-tabs-mode: nil -*-
# http://daringfireball.net/projects/markdown/syntax
#import xml.etree.ElementTree as etree
from lxml import etree
import re
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import ForeignKey

engine = create_engine('postgresql://pgserver.cs.huji.ac.il/public', echo=False)
Base = declarative_base(bind=engine)

def is_taham(c):
     return (c >= 1425 and c <= 1455) or c == 1472 or c == 1475

def is_nikud(letter):
        return letter >= 1456 and letter <= 1476

def to_nikud(verse):
     res = ''
     meta = False
     psik = False
     for c in verse:
          if c == '[':
               meta = True

          if meta:
             res += c
             if c == ']':
                  meta = False
          elif c == '׃':
                    res += '.'
          elif c == '־':
               res += ' '
          elif is_taham(ord(c)):
               if ord(c) == 1425:
                    psik = True
          elif c == ' ' and psik:
               psik = False
               res += ', '
          else:
               res += c
     res = re.sub('\[qk k=(.*) q=(.*)\]', '\1', res)
     return res

def to_tora(verse):
     res = ''
     meta = False
     for c in verse:
          if c == '[':
               meta = True

          if meta or ord(c) == 32:
             res += c
             if c == ']':
                  meta = False
          elif c == '־':
             res += ' '

          elif not (is_taham(ord(c)) or is_nikud(ord(c))): 
               res += c
               
     res = re.sub('\[qk k=(.*) q=(.*)\]', '\2', res)
     return res
          
class Verses(Base):
     __tablename__ = 'verses'
     id = Column(Integer, Sequence('verse_num'), primary_key=True)
     verse = Column(String, nullable=False)
     verse_nikud = Column(String, nullable=False)
     verse_tora = Column(String, nullable=False)

     def __init__(self, verse):
#         self.id = None
#             
         self.verse = verse
         self.verse_nikud = to_nikud(verse)
         self.verse_tora = to_tora(verse)
         
     def __repr__(self):
        return "<Verse('%s','%s')>" % (self.id, self.verse)

class Books(Base):
     __tablename__ = 'books'
     id = Column(Integer, Sequence('book_num'), primary_key=True)
     name = Column(String, nullable=False)
     hname = Column(String, nullable=False)
     start = Column(Integer, ForeignKey('verses.id'))
     part  = Column(String, nullable=False)
     
     def __init__(self, name, hname, start, part):
#         self.id = None
         self.name = name
         self.hname = hname
         self.start = start
         self.part = part

     def __repr__(self):
        return "<Book('%s', '%s','%s')>" % (self.id, self.name, self.start)

class Parashas(Base):
     __tablename__ = 'parashas'
     verse_id = Column(Integer, ForeignKey('verses.id'))
     book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
     pnum = Column(Integer, nullable=False, primary_key=True)

     def __init__(self, bid, pnum, vid):
         self.book_id = bid
         self.pnum = pnum
         self.verse_id = vid

     def __repr__(self):
        return "<Parsha('%s','%s', '%s')>" % (str(self.verse_id[0]), self.book_id, self.pnum)

def parsebook(session, books):
    pnum = 0 # couting open parashut relative to book
    snum = 0 # couting parsha sgura instead the open ones
    global vid # counting verses
    global bid # counting books
    plist = [] # list of open parashas
    verses = []
    bid += 1
    new = True
    
    for fname in book.find("filename").text.split(','):
        print(fname)
        verses.extend(etree.parse(fname+ '.xml').iterfind('*/book/c/v'))

    
    for verse in verses:
        if new:
             v = "[book name="+book.find("hebrewname").text+"]"
        else:
             v = ""
        vid += 1
        for elem in verse:
            if elem.tag == "w":
                v += re.compile('/').sub('',elem.text)
                if elem.text[-1] != '־':
                     v+= " "
            elif elem.tag == "pe":
                pnum += 1
                v += " [pe num="+str(pnum) +"]"
                snum = 0
                plist.append(Parashas(bid, pnum, vid))
            elif elem.tag == "samekh":
                 snum +=1
                 v += " [ps num="+str(snum) +"]"
            elif elem.tag == "q":
                 v += " q=" +re.compile('/').sub('',elem.text) + "] "
            elif elem.tag == "k":
                 v += " [qk k=" +re.compile('/').sub('',elem.text)
            elif elem.text is None:
                v += elem.tag
            else:
                v += " ["+elem.tag +"] " + re.compile('/').sub('',elem.text) +" ["+elem.tag +"/]"

            
        session.add(Verses(verse=v))
        session.commit()
        
        if new:
             session.add(Books(book.find("name").text, book.find("hebrewname").text,
                               vid, book.find("part").text))
             session.commit()
             new = False

        for p in plist:
             session.add(p)
        plist = []
        session.commit()
#        print(v)

# Main
Base.metadata.drop_all(engine) 
Base.metadata.create_all(engine) 
smaker = sessionmaker(bind=engine)
session = smaker()
#print(to_tora("[book name=בראשית]בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃"))
#exit(1)
vid = 0
bid = 0
books = etree.parse('JTanach.xml').findall('*/*/names')

for book in books: 
    parsebook(session, book)

#print(session.query(Verses).get(2))
#print(session.query(Parashas).get(('Genesis', 2)))

#employees.create(engine, checkfirst=True)
#employees.drop(engine, checkfirst=False)

