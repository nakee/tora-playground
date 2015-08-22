from django.db import models

# Create your models here.
class Verse(models.Model):
   full = models.CharField(max_length=500)
   nikkud = models.CharField(max_length=500)
   stripped = models.CharField(max_length=500)

