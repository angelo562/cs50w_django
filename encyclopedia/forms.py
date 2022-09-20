from logging import PlaceHolder
from django import forms

# Create forms here

class SearchForm(forms.Form):
    """ Form Class for Search Bar """  
    q = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Search Encyclopedia",}
      ))

class CreateEntry(forms.Form):
    """ Form class to create a new Entry"""
    title = forms.CharField(label="Entry Title", widget=forms.TextInput(attrs={
        "placeholder": "Enter Entry Title",
    }))
    body = forms.CharField(label="Body", widget=forms.Textarea(attrs={
        'class': "form-control",
        'rows': 3, 
        'cols': 10,
        "placeholder": "Enter content using Markdown",
    }))

class EditEntry(forms.Form):
    """ Form class to edit an existing Entry"""
    entry = forms.CharField(label="Entry", widget=forms.Textarea(attrs={
        'class': "form-control",
        'rows':15,
    }))