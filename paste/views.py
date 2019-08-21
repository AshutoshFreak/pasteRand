from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.views.generic import CreateView, DetailView

from .forms import PasteForm
from .models import PasteFile


class Index(CreateView):
    model = PasteFile
    form_class = PasteForm

    def form_valid(self, form):
        instance = form.save()
        form.save()
        return HttpResponseRedirect(instance.get_absolute_url())


class Detail(DetailView):
    template_name = "paste/index.html"
    model = PasteFile

    def get(self, request, slug):
        paste_obj = get_object_or_404(PasteFile, slug=slug)
        paste_content = {
            "title": paste_obj.title,
            "content": paste_obj.content,
            "date_time": paste_obj.date_time,
        }
        return render(request, template_name, paste_content)
