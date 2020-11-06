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
    entries = util.list_entries()
    if is_new:
        if request.method == "POST":
            form = newEntryForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                if title in entries:
                    return render(request, "encyclopedia/text_area.html", {
                        "form": searchForm(),
                        "hid": "visible",
                        "eform": form
                    })
                else:
                    util.save_entry(title, form.cleaned_data["text"])
                    return HttpResponseRedirect(reverse(index, args = (title, )))
            else:
                return render(request, "encyclopedia/text_area.html", {
                    "form": searchForm(), 
                    "hid": "hidden",
                    "eform": form
                })
        else:
            return render(request, "encyclopedia/text_area.html", {
                "form": searchForm(), 
                "hid": "hidden",
                "eform": newEntryForm()
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
                found_entries = []
                for entry in entries:
                    if title in entry.upper():
                        found_entries.append(entry)
                return render(request, "encyclopedia/search.html", {
                    "entries": found_entries, 
                    "form": form
                })
        return render(request, "encyclopedia/index.html", {
            "entries": entries, 
            "form": form
            })