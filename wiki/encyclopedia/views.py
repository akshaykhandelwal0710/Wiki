from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
import random
import markdown2

from . import util

class searchForm(forms.Form):
    search = forms.CharField()

class newEntryForm(forms.Form):
    title = forms.CharField(label = "Title")
    text = forms.CharField(widget = forms.Textarea, label = "Markdown")

def index(request, title = ""):
    entries = util.list_entries()
    if request.method == "POST":
        form = searchForm(request.POST)
        form.is_valid()
        return HttpResponseRedirect(reverse(index, args = (form.cleaned_data["search"],)))
    else:
        form = searchForm()
        if title:
            title = title.upper()
            ent = None
            for entry in entries:
                if entry.upper() == title:
                     ent = util.get_entry(entry)
            if ent:
                entry = markdown2.markdown(entry)
                return render(request, "encyclopedia/title.html", {
                    "entry": ent, 
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

def new(request):
    entries = util.list_entries()
    if request.method == "POST":
        form = newEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            title = title.lower()
            for i in range(len(entries)):
                entries[i] = entries[i].lower()
            if title in entries:
                return render(request, "encyclopedia/text_area.html", {
                        "form": searchForm(),
                        "hid": "visible",
                        "eform": form
                    })
            else:
                title = title[0].upper() + title[1:]
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

def rand(request):
    entries = util.list_entries()
    l = len(entries)
    x = random.randint(0, l - 1)
    return HttpResponseRedirect(reverse(index, args = (entries[x], )))
