from django.shortcuts import render
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from . import util
from .forms import SearchForm
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger()

def index(request):
    """ Returns the home/index page """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'search_form': SearchForm(),
    })

def display(request, title):
    """ Displays the page for each entry if an entry.md exists"""

    logger.debug(f"request is {request} of type {type(request)}")
    markdowner = Markdown()
    
    if util.get_entry(title):
        logger.debug(f"hello, i'm a logger. title is {title}")

        return render(request, "encyclopedia/entry.html",{ # Entry template
            "entry": markdowner.convert(util.get_entry(title)),
            "entry_title": title, #TODO make CSS all capitalized.
        })

    # Displays error page if entry doesn't exist
    else:
        return render(request, "encyclopedia/404page.html")

def search(request):
    """ Searches entries for a match or returns substrings?"""
    GET_value = request.GET.get('q','QueryNotFound')

    if util.get_entry(GET_value):
        return HttpResponseRedirect(f"{GET_value}")
    else:
        substr_matches = []
        for entry in util.list_entries():
            if GET_value.lower() in entry.lower():
                substr_matches.append(entry)
        
        return render(request, "encyclopedia/entry.html", {
            'entries': substr_matches,
            'GET_value': GET_value,
            'search':True
        })