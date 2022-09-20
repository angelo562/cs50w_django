from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from . import util
from .forms import CreateEntry, SearchForm
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
    """    Returns a create/edit page    """
    
    if request.method == "POST":
        form = CreateEntry(request.POST)
        logger.warning(f"form has been created")
        if form.is_valid():
            logger.warning(f"form is valid")

            title, body = form.cleaned_data['title'], form.cleaned_data['body']

            if util.get_entry(title):


                #TODO present error message
                messages.error(request, 'Page already exists. Please edit instead.')

                
                logger.warning(f"attempting to present msg to user {messages.error}")
                return render(request, 'encyclopedia/modify.html',{
                    "create_form": form,
                })
            #  use title and body to save as {title}.md file.  using util.py Will save over any existing entry
            util.save_entry(title, body)

            # redirect to index
            return redirect(reverse('encyclopedia:url_index'))




        # TODO if entry does exist, REDIRECT? to entry page

        pass
    
    return render(request, "encyclopedia/modify.html", {
        "create_form": CreateEntry()
    })

def edit(request):
    """ edits the page """

# TODO ADD AN EDIT BUTTON TO THE DISPLAY PAGE
def display(request, entry_title):
    """ Displays the page for each entry if an entry.md exists"""
    logger.info(f"request is {request} of type {type(request)}")

    markdowner = Markdown()

    if util.get_entry(entry_title):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(util.get_entry(entry_title)),
            "entry_title": entry_title,  # TODO make CSS all capitalized.
        })

    else:
        return render(request, "encyclopedia/404page.html")  # Error Page


def search(request):
    """ Searches for an exact entry  match or returns closest matches if exact entry not found
    """

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            GET_value = form.cleaned_data["q"]

            # if an entry exists redirects to "{GET_value}"
            if util.get_entry(GET_value):
                return HttpResponseRedirect(f"{GET_value}")

            else:
                return render(request, "encyclopedia/index.html", {
                    'entries': util.get_close_matches(GET_value),
                    'GET_value': GET_value,
                    'search': True
                })

    # Server side validation of GET response. Else redirects to index
    return redirect(reverse('encyclopedia:url_index'))
