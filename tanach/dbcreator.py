import PyQt5
import sqlalchemy
import sys
#import openpyxl
from openpyxl import load_workbook
import re
_author__ = 'nakee'

START_REMARK = "מ:אין פרשה בתחילת פרק"
NEW_BOOK = "מ:ספר חדש"
PARASHA_OPEN = "פפ"
PARASHA_CLOSE = "סס"
NOSACH = "נוסח"
SPACE = "ר4"
PASEK = "מ:פסק"
LEGARMIA = "מ:לגרמיה"

class Parser:

    def __init__(self):
        self.wb = load_workbook('Miqra_al_pi_ha-Mesorah.xlsx')
        self.parts = ["תורה", "נביאים ראשונים", "נביאים אחרונים", "ספרי אמ\"ת", "חמש מגילות", "כתובים אחרונים"]
        self.booknum = 1
        self.book = None

    def close_book(self):
        self.book.write('</book>\n</tanach>\n')

    def new_book(self, bookname):

        if self.book is not None:
            self.close_book()
        num = str(self.booknum)
        print("Creating book " + num + ": " +bookname)
        fname = num+bookname+'.xml'
        self.book = open('out/'+fname,'w',encoding="UTF-8")
        self.book.write('<?xml version = "1.0" encoding="UTF-8"?>\n')
        self.book.write('<tanach>\n<book>\n<names>\n')
        self.book.write('<teiHeader>\n')
        self.book.write('<name>'+bookname+'</name>\n')
        self.book.write('<number>'+num+'</number>\n')
        self.book.write('<filename>'+fname+'</filename>\n')
        self.book.write('</names>\n')
        self.book.write('</teiHeader>\n')

        self.booknum += 1

    def parse_tags(self, tags):

        if tags is None or  "__" in tags:
            return

        # get rid of nosach tags for now
        tags =  re.sub('{{'+NOSACH+'\|(.*?)\|.*}}','\g<1>', tags)

        # find all tags
        m = re.findall("{{(.*?)}}", tags)

        for tag in m:
            if START_REMARK in tag:
                continue
            elif NEW_BOOK in tag:
                self.new_book(re.sub(NEW_BOOK+'\|', '', tag))
            elif PARASHA_OPEN in tag:
                self.book.write("<pe />\n")
            elif PARASHA_CLOSE in tag:
                self.book.write("<ps />\n")
            elif SPACE in tag:
                self.book.write("<4space />\n")
#            else:
#                print(tag)



    def parse_pasuk(self, res):

        if row[4].value is None:
            return

        res = re.sub('{{'+PASEK+'}}','<pasek />' , res) # chr(0x05C0)
        res = re.sub('{{'+LEGARMIA+'}}', '<legarmeih />', res)

        BIG_LETTER="מ:אות-ג"
        SMALL_LETTER="מ:אות-ק"

        # more complex
        pasuk1 = res
        res = re.sub('{{'+BIG_LETTER+'.*\|.*?=*(.*?)}}','<special type=big>\g<1></special>',res)

        if pasuk1 != res:
            print("" + res + "\n" + pasuk1)

        res = re.sub('{{'+SMALL_LETTER+'.*\|.*?=*(.*?)}}','<special type=small>\g<1></special>',res)
        res = re.sub('{{'+NOSACH+'\|(.*?)\|.*}}','\g<1>' ,res)
        res = re.sub('{{קמץ\|.*=(.*?)\|.*}}','\g<1>' ,res)
        res = re.sub('{{כו"ק\|(.*?)\|(.*?)\|.*}}','<qk q="\g<1>" k="\g<2>">' ,res)

         # get rid of nosach tags for now
#        pasuk1 =  re.sub('{{'+NOSACH+'\|(.*?)\|.*}}','\g<1>', res)

        # find all tags
        #m = re.findall("{{(.*?)}}", tags)


        #for tag in m:
        #    print(tag)

        self.book.write(res +'\n')


if __name__ == "__main__":
    parser = Parser()
    for part in parser.parts:
        ws = parser.wb.get_sheet_by_name(part)
        for row in ws.rows:
            # ignore Dovi's remarks for now
            if row[4].value is not None:
                parser.parse_tags(row[2].value)

            parser.parse_pasuk(row[4].value)
