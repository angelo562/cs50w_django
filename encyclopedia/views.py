from django.shortcuts import render, redirect
from django.urls import reverse
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

def create(request):
    """
    Returns a create/edit page
    """
    return render(request, "encyclopedia/modify.html")

def display(request, title):
    """ Displays the page for each entry if an entry.md exists"""
    logger.debug(f"request is {request} of type {type(request)}")

    markdowner = Markdown()
    
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html",{ 
            "entry": markdowner.convert(util.get_entry(title)),
            "entry_title": title, #TODO make CSS all capitalized.
        })

    # Displays error page if entry doesn't exist
    else:
        return render(request, "encyclopedia/404page.html")

def search(request):
    """ Searches for an exact entry  match or returns closest matches if exact entry not found
    """

    if request.method == 'GET':
        GET_value = request.GET.get('q','QueryNotFound')
        logger.warning(f"request.GET is {request.GET}")


        # if an entry exists redirects to "/wiki/{GET_value}"
        if util.get_entry(GET_value):
            return HttpResponseRedirect(f"{GET_value}")

        else:
            return render(request, "encyclopedia/index.html", {
                'entries': util.get_close_matches(GET_value),
                'GET_value': GET_value,
                'search':True
            })

    return redirect(reverse('encyclopedia:url_index'))