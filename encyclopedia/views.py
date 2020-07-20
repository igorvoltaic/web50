from django.views.defaults import page_not_found
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.urls import reverse

from markdown2 import markdown
import random as rand

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'style': 'height:400px;'}),label="Entry Content")

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.lower() in [x.lower() for x in util.list_entries()]:
            raise forms.ValidationError("You already have such entry!")
        return title


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if not util.get_entry(title):
       return page_not_found(request, True, template_name="404.html")
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown(util.get_entry(title))
    })


def search(request):
    q = request.GET['q']
    if q.lower() in [x.lower() for x in util.list_entries()]:
        return HttpResponseRedirect(reverse('entry', args=[q]))
    entries = []
    for word in util.list_entries():
        if q.lower() in word.lower():
            entries.append(word)
    return render(request, "encyclopedia/index.html", {
        "results": True,
        "entries": entries
    })

def random(request):
    title = rand.choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown(util.get_entry(title))
    })


def edit(request, title=None):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if not title:
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
            else:
                return render(request, "encyclopedia/create.html", {
                    "form": form
                })
        elif title == form.data['title']:
            title = form.data['title']
            content = form.data['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entry', args=[title]))
    if not title:
        return render(request, "encyclopedia/create.html", {
            "form": NewEntryForm()
        })
    data = {'title': title, 'content': util.get_entry(title)}
    populated_form = NewEntryForm(initial=data)
    return render(request, "encyclopedia/create.html", {
        "edit": True,
        "title": title,
        "form": populated_form
    })

