from unittest import TestCase
from dbcreator import Parser


__author__ = 'nakee'


class TestParser(TestCase):

  parser = Parser()

  def test_parse_big(self):
    print("calling function: "+self.parser.parse_verse("{{מ:אות-ג|בְּ}}"))
    self.assertEqual( "<big>בְּ</big>", self.parser.parse_verse("{{מ:אות-ג|בְּ}}"))

  def test_parse_kriktiv(self):
    self.assertEqual("", self.parser.parse_verse('{{קו"כ-אם|עִירֹ֔ה|ל-קרי=עִיר֔וֹ}}'))
