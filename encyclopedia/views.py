from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from . import util
from .forms import CreateEntry, SearchForm, EditEntry
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

                return render(request, 'encyclopedia/create.html', {
                    "create_form": form,
                    "title":title
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


def edit(request,title):
    """ edits the page """
    if request.method == "POST":
        logger.warning(f"Checking request.method {request.method}")

        form = EditEntry(request.POST)
        logger.warning(f"Checking form. form is {form}")

        logger.warning(f"is form valid? {form.is_valid()}")
        if form.is_valid():
            entry = form.cleaned_data['entry']
            util.save_entry(title, entry)

            logger.warning(f"attempting to go to index after save")
            return redirect(reverse('encyclopedia:url_display', kwargs={
                'entry_title':title,
            }))


    # Display edit page with Django text. 
    return render(request, "encyclopedia/edit.html", {
        'entry_title': title,
        'search_form': SearchForm(),
        'edit': True,
        "edit_form" : EditEntry({"entry": util.get_entry(title)}) #pop needs dict
    })

def display(request, entry_title):
    """ Displays the page for each entry if an entry.md exists"""
    logger.info(f"request is {request} of type {type(request)}")
    
    markdowner = Markdown()

    if util.get_entry(entry_title):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(util.get_entry(entry_title)),
            "entry_title": entry_title,  
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
