from django.db import models
import re

# Create your models here.
def parse_verse(verse):
    verse = re.sub('\[open-parasha num="(\d+)"\]', '<br /><br /><b>\g<1>. </b>', verse)
    return verse

class Verse(models.Model):
    full = models.CharField(max_length=500)
    nikkud = models.CharField(max_length=500)
    stripped = models.CharField(max_length=500)

    def get_verse(self):
        return parse_verse(self.full)