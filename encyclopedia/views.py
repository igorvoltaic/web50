from django.http import Http404
from django.views.defaults import page_not_found
from django.shortcuts import render
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if not util.get_entry(title):
        return page_not_found(request, True, template_name='404.html')
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown(util.get_entry(title))
    })
