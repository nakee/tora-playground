from django.db import models
import re

# Create your models here.
class Verse(models.Model):
    full = models.CharField(max_length=500)
    nikkud = models.CharField(max_length=500)
    stripped = models.CharField(max_length=500)

    def get_verse(self):
        res = re.sub('ׇ',  '<kamatz-katan>ׇ</kamatz-katan>', self.full)
        return res


class Books(models.Model):
    name = models.CharField(max_length=100)
    start = models.ForeignKey(Verse)

#class divitions(models.Model):
#    group_id = models.IntegerField()
#    start = models.ForeignKey(Verse)
#    end = models.ForeignKey(Verse)
#    comment = models.CharField(max_length=500)
