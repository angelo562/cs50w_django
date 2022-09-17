from django import forms

class SearchForm(forms.Form):
    """ Form Class for Search Bar """  
    # Research why this works.
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Search Encyclopedia"}))