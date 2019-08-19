from django.shortcuts import HttpResponseRedirect, get_object_or_404, render

from .forms import PasteForm
from .models import PasteFile


def index(request):
    if request.method == "POST":
        form = PasteForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        form = PasteForm()

    return render(request, "paste/index.html", {"form": form})


def detail(request, slug):
    paste = get_object_or_404(PasteFile, slug=slug)
    context = {"title": paste.title, "content": paste.content}
    return render(request, "paste/detail.html", context)
