from django.shortcuts import render,redirect

from . import util
import markdown2
from random import choice

from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title:", widget = forms.Textarea(attrs={"style":"width:600px; height:26px;", "id":"entry-title"}))
    content = forms.CharField(label="Content:", initial="You may use markdown styling.", widget = forms.Textarea(attrs={"style":"width:600px; height:150px;"}))

class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search")


def index(request):
    search_for = request.GET.get("q")
    if search_for:
        entries = util.list_entries()
        for item in entries:
            if search_for.upper() == item.upper():
                return redirect('/wiki/{0}'.format(item))
        new_list = []
        for item in entries:
            if search_for.upper() in item.upper():
                new_list.append(item)
        return render(request, "encyclopedia/index.html",{
            "entries": new_list
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def search_result(request):
    if request.method == "POST":
        entries = util.list_entries()
        new_list = []
        search_for = request.POST.get("search")

        for item in entries:
            if search_for.upper() in item.upper():
                new_list.append(item)
        return render(request, "encyclopedia/index.html",{
            "entries": new_list
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "form" : NewSearchForm()
        }) 

def entry(request, title):
    if util.get_entry(title):
        entry = markdown2.markdown(util.get_entry(title))
    else:
        return render(request,"encyclopedia/add.html", {
            "form": NewEntryForm(),
            "comment":"<h3 style=\"color:brown\">Not found. Would you like to add entry.</h3>"
            }) 
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })

def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        entry_list = util.list_entries()
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            content = "#"+title+"\n\n"+content
            if title not in entry_list:
                util.save_entry(title, content)
                return redirect('/wiki/{0}'.format(title))
            else:
                entry = util.get_entry(title)
                form = NewEntryForm(initial={"title":title, "content":entry}, )
                return render(request, "encyclopedia/edit.html", {"form":form,"comment":"These entry is currently in wiki, would you like to edit it?"})
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": NewEntryForm()
        })


def edit(request, title):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('/wiki/{0}'.format(title))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
        })
    else:
        entry = util.get_entry(title)
        form = NewEntryForm(initial={"title":title, "content":entry})
        return render(request, "encyclopedia/edit.html", {
            "form":form,
        })

def random(request):
    entry_list = util.list_entries()
    title = choice(entry_list)
    return redirect('/wiki/{0}'.format(title))
