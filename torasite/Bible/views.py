from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
import re

# Create your views here.
from django.http import HttpResponse
from bible.models import Verse

def index(request):

    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    verse_list = Verse.objects.all()
    paginator = Paginator(verse_list, 42) # Show 42 verses per page

    page = request.GET.get('page')
    try:
        verses = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        verses = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        verses = paginator.page(paginator.num_pages)

    return render_to_response('bible/bible.html', {"verses": verses})
