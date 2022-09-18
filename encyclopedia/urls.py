from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="url_index"),

    # I can send the submitted query to any path.
    path("search", views.search, name="url_search"),
    path("<str:title>", views.display, name="url_display"), 
        # Matches str before ".html"
    path("modify", views.create, name="url_modify"),
    
]
