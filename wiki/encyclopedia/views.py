from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util

class searchForm(forms.Form):
    search = forms.CharField()

class newEntryForm(forms.Form):
    title = forms.CharField(label = "Title")
    text = forms.Textarea()

def index(request, title = "", is_new = False):
    if is_new:
        if request.method == "POST":
            pass
        else:
            return render(request, "encyclopedia/text_area.html" {
                "form": searchForm(), 
                "hid": "hidden"
            })
    elif request.method == "POST":
        form = searchForm(request.POST)
        form.is_valid()
        return HttpResponseRedirect(reverse(index, args = (form.cleaned_data["search"],)))
    else:
        form = searchForm()
        if title:
            title = title.upper()
            entry = util.get_entry(title)
            if entry:
                return render(request, "encyclopedia/title.html", {
                    "entry": entry, 
                    "title": title,
                    "form": form
                })
            else:
                entries = util.list_entries()
                found_entries = []
                for entry in entries:
                    if title in entry.upper():
                        found_entries.append(entry)
                return render(request, "encyclopedia/search.html", {
                    "entries": found_entries, 
                    "form": form
                })
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), 
            "form": form
            })