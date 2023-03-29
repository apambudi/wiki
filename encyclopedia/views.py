from django.shortcuts import render
from . import util
import random
import markdown2
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

class NewPage(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)

# Show list of encyclopedia entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Show an entry page:
def show_entry(request, title):
    content = util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/show_entry.html", {
            "content": False
        })
    else:
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/show_entry.html", {
            "content": html_content
        })

# Search a page:
def search(request):
    query = request.POST['q']
    entries = util.list_entries()
    if query.lower() in [x.lower() for x in entries]:
        return show_entry(request, query)
    else:
        sub_entries = []
        [sub_entries.append(entry) for entry in entries if query in entry]
        return render(request, "encyclopedia/search.html", {
            "entries": sub_entries
        })

# Add a new page:
def new_page(request):

    # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewPage(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the title from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = [x.lower() for x in util.list_entries()]
            if title.lower() in entries:
                return HttpResponse("Error 403: The encyclopedia entry already exists")
            else:
                util.save_entry(title, content)
                return show_entry(request, title)

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/new_page.html", {
                "page": NewPage()
            })

    return render(request, "encyclopedia/new_page.html", {
        "form": NewPage()
    })

# Show list of entries for edit page 
def edit_page(request):
    return render(request, "encyclopedia/edit_page.html", {
        "entries": util.list_entries()
    })

# Edit a page
def edit_content(request, title):
    content = util.get_entry(title)
    page = NewPage(initial={'title': title, 'content': content})

    # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewPage(request.POST)
        
        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the title from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Save the updated page 
            util.save_entry(title, content)

            # Redirect user to the entry's page
            return show_entry(request, title)
            # HttpResponseRedirect(reverse("show_entry", args=(title,)))
        
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/edit_content.html", {
                "form": page
            })

    return render(request, "encyclopedia/edit_content.html", {
    "form": page, "title": title
    })

# Show a random page
def random_page(request):
    entries = util.list_entries()
    index = random.randint(0, len(entries) - 1)
    title = entries[index]
    return show_entry(request, title)