from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.
from django.http import HttpResponse
from Bible.models import Verse

def index(request):

    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    contact_list = Verse.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render_to_response('bible/bible.html', {"contacts": contacts})
