from django import forms

# Create forms here

class SearchForm(forms.Form):
    """ Form Class for Search Bar """  
    # Research why this works.
    q = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Search Encyclopedia",}
      ))