from hashlib import new
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util
from django import forms
from markdown2 import Markdown
from random import randint

class PageForm(forms.Form):
    title = forms.CharField(label = "New Entry Title")
    content = forms.CharField(widget=forms.Textarea)

class editForm(forms.Form):
    new_content = forms.CharField(widget =forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title not in util.list_entries():
        top = "404: Page Not Found."
        error = "Sorry, the page you tried to go to does not exist."
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "top": top,
            "error": error
        })
    else:
        markdowner = Markdown()
        content = markdowner.convert(util.get_entry(title))
        raw_content = util.get_entry(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content,
            "raw_content": raw_content
        })

def searchResults(request):
    if request.method == "POST":
        if request.POST["q"] not in util.list_entries():
            resultList = [k for k in util.list_entries() if request.POST["q"] in k ]
            return render(request, "encyclopedia/searchResults.html", {
                "input": request.POST["q"],
                "resultList": resultList
            })
        else:
            markdowner = Markdown()
            title = request.POST["q"]
            content = markdowner.convert(util.get_entry(title))
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content
            })
    else:
        return render(request, "encyclopedia/clown.html")

def newPage(request):
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["title"]
            new_content = form.cleaned_data["content"]

            if new_title in util.list_entries():
                top = "Page already exists."
                error = "Sorry, the page you tried to create already exists. "
                return render(request, "encyclopedia/error.html", {
                    "top": top,
                    "error": error,
                    "title": new_title
                })
            else:
                markdowner = Markdown()
                util.save_entry(new_title, new_content)
                return render(request, "encyclopedia/entry.html", {
                    "title": new_title,
                    "content": markdowner.convert(new_content)
                })

    else:
        form = PageForm()
        return render(request, "encyclopedia/newPage.html", {
            "title": "New Page",
            "form": form
        })

def editPage(request, title):
    if request.method == "POST":
        new_content = request.POST["new_content"]
        util.save_entry(title, new_content)

        markdowner = Markdown()
        updated_content = markdowner.convert(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": updated_content
        })

    else:
        raw_content = util.get_entry(title)
        return render(request, "encyclopedia/editPage.html", {
            "form": editForm({'new_content': raw_content}),
            "title": title
        })

def randomPage(request):
    number = randint(0, len(util.list_entries()) - 1)
    pageList = util.list_entries()
    title = pageList[number]
    markdowner = Markdown()
    content = markdowner.convert(util.get_entry(title))
    return render(request, 'encyclopedia/entry.html', {
        "title": title,
        "content": content
    })

