from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from . import util
from .forms import CreateEntry, SearchForm, EditEntry
import logging
from random import choice

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

            # If entry exists, Error msg and stay on form page
            if util.get_entry(title):
                messages.error(
                    request, 'Page already exists. Please edit using link below instead.')
                return render(request, 'encyclopedia/create.html', {
                    "create_form": form,
                    "title": title
                })
            else:
                util.save_entry(title, body)
                return redirect(reverse('encyclopedia:url_index'))

        else:
            messages.error(request, 'Form is not valid')
    return render(request, "encyclopedia/create.html", {
        "create_form": CreateEntry(),
        'search_form': SearchForm(),
    })


def edit(request, title):
    """ Edits the page """
    if request.method == "POST":
        form = EditEntry(request.POST)
        if form.is_valid():
            entry = form.cleaned_data['entry']
            util.save_entry(title, entry)
            return display(request, title)

    # Display edit page with Django text.
    return render(request, "encyclopedia/entry.html", {
        'entry_title': title,
        'search_form': SearchForm(),
        'edit': True,
        # If populating form, needs dict of the key to populate
        "edit_form": EditEntry({"entry": util.get_entry(title)}) 
    })


def display(request, entry_title):
    """ Displays the page for each entry if an entry.md exists"""

    markdowner = Markdown()
    if util.get_entry(entry_title):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(util.get_entry(entry_title)),
            "entry_title": entry_title,
            'search_form': SearchForm(),
            'edit': False,
        })

    else:
        return render(request, "encyclopedia/404page.html")  # Error Page


def search(request):
    """ Searches for an exact entry  match or returns closest matches if exact entry not found
    """

    if request.method == 'GET':
        form = SearchForm(request.GET)

        # Server side validation of GET response. Else redirects to index
        if form.is_valid():
            GET_value = form.cleaned_data["q"]

            if util.get_entry(GET_value):           # If entry exists
                return display(request, GET_value)

            else:
                return render(request, "encyclopedia/index.html", {
                    'entries': util.get_close_matches(GET_value),
                    'GET_value': GET_value,
                    'search': True
                })

    return index(request)


def get_random(request):
    """ If random page is clicked, will randomly select an entry"""

    return display(request, choice(util.list_entries()))
