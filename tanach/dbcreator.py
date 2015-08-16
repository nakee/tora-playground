#import sqlalchemy
#import sys
from openpyxl import load_workbook
import re
_author__ = 'nakee'

# editor can't handle hebrew
START_REMARK = "מ:אין פרשה בתחילת פרק"
NEW_BOOK = "מ:ספר חדש"
PARASHA_OPEN = "פפ"
PARASHA_CLOSE = "סס"
NOSACH = "נוסח"
SUBBOOK = "רווח"
SPACE0 = "ר0"
SPACE1 = "ר1"
SPACE2 = "ר2"
SPACE3 = "ר3"
SPACE4 = "ר4"
ATNACH_UPSIDE = "אתנח הפוך"
COMMENT = "הערה"
FONT_SIZE = "גודל גופן"
PASEK = "מ:פסק"
LEGARMIA = "מ:לגרמיה"
BIG_LETTER = "מ:אות-ג"
SMALL_LETTER = "מ:אות-ק"
KAMATZ = "קמץ"
KRIKTIV = 'קו"כ'
KTIVKRI = 'כו"ק'
KRIKTIVEM = 'קו"כ-אם'
DOTS = "מ:אות מנוקדת"
HANG = "מ:אות תלויה"
GALGAL = "גלגל"
YARECH = "ירח בן יומו"



class Parser:

    def __init__(self):
        self.wb = load_workbook('Miqra_al_pi_ha-Mesorah.xlsx')
        self.parts = ["תורה", "נביאים ראשונים", "נביאים אחרונים", "ספרי אמ\"ת", "חמש מגילות", "כתובים אחרונים"]
        self.booknum = 1
        self.book = None

    def close_book(self):
        self.book.write('</book>\n</bible>\n')

    def new_book(self, book_name):

        if self.book is not None:
            self.close_book()
        num = str(self.booknum)
        print("Creating book " + num + ": " + book_name)
        file_name = num + book_name + '.xml'
        self.book = open('out/' + file_name, 'w', encoding="UTF-8")
        self.book.write('<?xml version = "1.0" encoding="UTF-8"?>\n')
        self.book.write('<bible>\n<book>\n')
        self.book.write('<teiHeader>\n')
        self.book.write('<names>\n')
        self.book.write('<name>' + book_name + '</name>\n')
        self.book.write('<number>' + num + '</number>\n')
        self.book.write('<filename>' + file_name + '</filename>\n')
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
                self.book.write("<open-parasha />\n")
            elif PARASHA_CLOSE in tag:
                self.book.write("<closed-parasha />\n")
            elif SPACE0 in tag:
                self.book.write("<0space />\n")
            elif SPACE1 in tag:
                self.book.write("<1space />\n")
            elif SPACE2 in tag:
                self.book.write("<2space />\n")
            elif SPACE3 in tag:
                self.book.write("<3space />\n")
            elif SPACE4 in tag:
                self.book.write("<4space />\n")
            elif SUBBOOK in tag:
                self.book.write("<sub-book />\n")
            else:
                print(tag)

    def parse_verse(self, res):

        m = re.match("(.*){{(.*?)}}(.*)", res)
        while m is not None:
#        if m is not None:
            res = m.group(1) + self.parse_verse(m.group(2)) + m.group(3)
    #        print("We parse "+m.group(2))
            m = re.match("(.*){{(.*?)}}(.*)", res)

        res = re.sub(PASEK,'<pasek />' , res) # chr(0x05C0)
        res = re.sub(LEGARMIA, '<legarmeih />', res)


        res = re.sub(FONT_SIZE+'.*','', res) #FIXME: get comments
        res = re.sub('.*?'+COMMENT+'\|(.*?)}+','<comment>\g<1></comment>', res)


        res = re.sub(PARASHA_OPEN+'+', '<open-parasha />', res)
        res = re.sub(PARASHA_CLOSE+'+', '<closed-parasha />', res)
        res = re.sub(SPACE0, '<0space />', res)
        res = re.sub(SPACE1, '<1space />', res)
        res = re.sub(SPACE2, '<2space />', res)
        res = re.sub(SPACE3, '<3space />', res)
        res = re.sub(SPACE4, '<4space />', res)
        res = re.sub(ATNACH_UPSIDE, '<upside-atnach />', res)
        res = re.sub(GALGAL, '<galgal />', res)
        res = re.sub(YARECH, '<yarech />', res)


        # more complex
        res = re.sub(BIG_LETTER+'.*\|.*?=*(.+)','<big>\g<1></big>', res)
        res = re.sub(SMALL_LETTER+'.*\|.*?=*(.+)','<small>\g<1></small>', res)
        res = re.sub(DOTS+'\|(.*?)\|.*','<dots>\g<1></dots>', res)
        res = re.sub(HANG+'\|(.+)','<hang>\g<1></hang>', res)
        res = re.sub(NOSACH+'\|(.*?)\|.*', '\g<1>', res)
        res = re.sub(KAMATZ+'\|.*=(.*?)\|.*','\g<1>', res)
 #       res = re.sub(KTIVKRI+'.*?\|(.+?)\|.*?=*(.+?)\|.*','<ktivkri ktiv="\g<1>" kri="\g<2>">', res)
        res = re.sub(KRIKTIVEM+'.*?\|(.+?)\|.*?\=([^\(]+).*','\g<1>', res)
        res = re.sub(KTIVKRI+'.*?\|(.+?)\|.*?\=*(.+)','<qereketiv qere="\g<2>" ketiv="\g<1>">', res)
        res = re.sub(KRIKTIV+'.*?\|(.+?)\|.*?\=*(.+)','<qereketiv qere="\g<2>" ketiv="\g<1>">', res)

    #    print("after " + res)
        return res

if __name__ == "__main__":
    parser = Parser()
    for part in parser.parts:
        ws = parser.wb.get_sheet_by_name(part)
        for row in ws.rows:

#            if parser.booknum > 2:
#                continue


            # ignore Dovi's remarks for now
            if row[4].value is not None  and row[1].value is not None:
                parser.parse_tags(row[2].value)

            if parser.book is not None and row[4].value is not None and row[1].value is not None:
                res = row[4].value
#                if '<' in res or '>' in res:
#                    print("function start " + res)
                parser.book.write("<verse>")
                parser.book.write(parser.parse_verse(row[4].value))
                parser.book.write('</verse>\n')

    parser.close_book()
