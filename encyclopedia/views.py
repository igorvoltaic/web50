from django.views.defaults import page_not_found
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.urls import reverse

from markdown2 import markdown
import random as rand

from . import util


class EntryForm(forms.Form):
    title = forms.CharField(label="Entry Title")
    content = forms.CharField(widget=forms.Textarea(),label="Entry Content")

    def new(self, new):
        self.new = None

    def clean_title(self):
        """ Check of the title already exists and raise an error if so.
        """
        title = self.cleaned_data['title']
        if not self.new and title.lower() in [x.lower() for x in util.list_entries()]:
            raise forms.ValidationError("You already have such entry!")
        return title


def index(request):
    """ Return the list of all wiki entries.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    """ Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry,
        renders a page that displays the contents of that encyclopedia entry.
    """
    if not util.get_entry(title):
       return page_not_found(request, True, template_name="404.html")
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown(util.get_entry(title))
    })


def search(request):
    """ Search for an wiki entry.
        If the query matches the name of an wiki entry, the user gets redirected to that entry’s page.
        If the query does not match the name of an wiki entry, takes the user to a search results page
        that displays a list of all wiki entries
    """
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
    """ Returns random wiki entry.
    """
    title = rand.choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown(util.get_entry(title))
    })


def edit(request, title=None):
    """ Returns EntryForm populated with existing wiki entry content for page the page being edited.
        If 'title' arg is not provided returns an empty form.
        On POST request form contents of the form get validated and saved to disk,
        and the user is taken to the entry’s page.
    """
    if request.method == "POST":
        form = EntryForm(request.POST)
        form.new = title  # for new Entry it keeps None value
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entry', args=[title]))
    if not title:
        return render(request, "encyclopedia/edit.html", {
            "form": EntryForm()
        })
    data = {'title': title, 'content': util.get_entry(title)}
    populated_form = EntryForm(initial=data)
    return render(request, "encyclopedia/edit.html", {
        "edit": True,
        "title": title,
        "form": populated_form
    })

