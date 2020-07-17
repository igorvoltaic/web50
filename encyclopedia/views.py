from django.views.defaults import page_not_found
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.urls import reverse

from markdown2 import markdown

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


def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry', args=[title]))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })


def search(request):
    q = request.GET['q']
    if q.lower() in [x.lower() for x in util.list_entries()]:
        return HttpResponseRedirect(reverse('entry', args=[q]))
    entries = []
    for word in [x for x in util.list_entries()]:
        if q.lower() in word.lower():
            entries.append(word)
    return render(request, "encyclopedia/index.html", {
        "results": True,
        "entries": entries
    })


