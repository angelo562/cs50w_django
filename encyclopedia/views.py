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
    """    Handles create page view    """

    if request.method == "POST":
        form = CreateEntry(request.POST)
        if form.is_valid():
            title, body = form.cleaned_data['title'], form.cleaned_data['body']

            if util.get_entry(title):
                # Error msg if existing template
                messages.error(
                    request, 'Page already exists. Please edit using link below instead.')

                return render(request, 'encyclopedia/modify.html', {
                    "create_form": form,
                    "title":title
                })
            else:
                util.save_entry(title, body)
                return redirect(reverse('encyclopedia:url_index'))

        else:
            messages.error(request, 'Form is not valid')
    return render(request, "encyclopedia/modify.html", {
        "create_form": CreateEntry(),
        'search_form': SearchForm(),
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
            'search_form': SearchForm(),
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
