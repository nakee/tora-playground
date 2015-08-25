__author__ = 'nakee'

import re

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



