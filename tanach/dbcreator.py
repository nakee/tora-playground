from openpyxl import load_workbook
import re
import trutils

_author__ = 'nakee'

DJANGO = "yes"
if DJANGO == "yes":
    import os
    import sys
    sys.path.append('../torasite/')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "torasite.settings")

    # your imports, e.g. Django models
    from Bible.models import Verse


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
HAFOCH = 'נו"ן הפוכה במקרא'
PARASHA_EMTZA = "פסקא באמצע פסוק"
DOUBLE = "שני טעמים באות אחת"

class Parser:

    def __init__(self):
        self.wb = load_workbook('Miqra_al_pi_ha-Mesorah.xlsx')
        self.parts = ["תורה", "נביאים ראשונים", "נביאים אחרונים", "ספרי אמ\"ת", "חמש מגילות", "כתובים אחרונים"]
        self.booknum = 1
        self.open = 0
        self.closed = 0
        self.book = None

    def close_book(self):
        self.book.write('</book>\n</bible>\n')

    def new_book(self, book_name):

        self.open = 0
        self.closed = 0

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

    def get_open_number(self):
        self.open += 1
        self.closed = 0
        return str(self.open)

    def get_closed_number(self):
        self.closed += 1
        return str(self.closed)

    def parse_verse(self, verse):

        if verse is None or  "__" in verse:
           return ''

        verse = re.sub('//', '', verse)
	
        m = re.match("(.*){{(.*?)}}(.*)", verse)
        while m is not None:
            verse = m.group(1) + self.parse_verse(m.group(2)) + m.group(3)
            m = re.match("(.*){{(.*?)}}(.*)", verse)

        if NEW_BOOK in verse:
            self.new_book(re.sub(NEW_BOOK+'\|', '', verse))
            return ''

        verse = re.sub(PASEK,'<pasek />' , verse) # chr(0x05C0)
        verse = re.sub(LEGARMIA, '<legarmeih />', verse)


        verse = re.sub(FONT_SIZE+'.*','', verse) #FIXME: get comments
        verse = re.sub('.*?'+COMMENT+'\|(.*?)}+','<comment>\g<1></comment>', verse)

        count = 0
        (verse, count) = re.subn(PARASHA_OPEN+'+', '<open-parasha num="', verse)
        if count > 0:
            verse += self.get_open_number() +'"/>'
        count = 0
        (verse, count) = re.subn(PARASHA_CLOSE+'+', '<closed-parasha num="', verse)
        if count > 0:
            verse += self.get_closed_number() +'"/>'

        verse = re.sub(SPACE0, '<0space />', verse)
        verse = re.sub(SPACE1, '<1space />', verse)
        verse = re.sub(SPACE2, '<2space />', verse)
        verse = re.sub(SPACE3, '<3space />', verse)
        verse = re.sub(SPACE4, '<4space />', verse)
        verse = re.sub(ATNACH_UPSIDE, '<upside-atnach />', verse)
        verse = re.sub(GALGAL, '<galgal />', verse)
        verse = re.sub(YARECH, '<yarech />', verse)


        # more complex
        verse = re.sub(BIG_LETTER+'.*\|.*?=*(.+)','<big>\g<1></big>', verse)
        verse = re.sub(SMALL_LETTER+'.*\|.*?=*(.+)','<small>\g<1></small>', verse)
        verse = re.sub(DOTS+'\|(.*?)\|.*','<dots>\g<1></dots>', verse)
        verse = re.sub(HANG+'\|(.+)','<hang>\g<1></hang>', verse)
        verse = re.sub(HAFOCH+'.*','<nun>׆</nun>', verse)
        verse = re.sub(NOSACH+'\|(.*?)\|.*', '\g<1>', verse)
        verse = re.sub(KAMATZ+'\|.*=(.*?)\|.*','\g<1>', verse)
        verse = re.sub(KRIKTIVEM+'.*?\|(.+?)\|.*?\=([^\(]+).*','\g<1>', verse)
        verse = re.sub(KTIVKRI+'.*?\|(.+?)\|.*?\=*(.+)','<qereketiv qere="\g<2>" ketiv="\g<1>" />', verse)
        verse = re.sub(KRIKTIV+'.*?\|(.+?)\|.*?\=*(.+)','<qereketiv qere="\g<2>" ketiv="\g<1>" />', verse)

        verse = re.sub(DOUBLE+'.*?\|(.+)\|(.+)', '<twomarks first="\g<1>" second="\g<2>" />', verse)
        return verse

if __name__ == "__main__":
    parser = Parser()
    for part in parser.parts:
        ws = parser.wb.get_sheet_by_name(part)
        for row in ws.rows:

#            if parser.booknum > 2:
#                continue

            if row[4].value is not None and row[1].value is not None:
                verse = parser.parse_verse(row[2].value) + parser.parse_verse(row[4].value)
                parser.book.write("<verse>" + verse + "</verse>\n")
                if DJANGO == "yes":
                    verse = re.sub('<', '[', verse)
                    verse = re.sub('>', ']', verse)
                    verse = re.sub('/', '', verse)
                    v = Verse(full=verse, nikkud=trutils.to_nikud(verse), stripped=trutils.to_tora(verse))
#                    print(verse)
                    v.save()

    parser.close_book()
