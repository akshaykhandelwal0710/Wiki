from django.shortcuts import render
from django.http import HttpResponse

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    title = title.upper()
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/title.html", {
            "entry": entry, 
            "title": title
        })
    else:
        return HttpResponse("Error! Page not found...")