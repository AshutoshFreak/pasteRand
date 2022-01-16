from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.http import HttpResponse

from .forms import CommentForm, PasteForm
from .models import Comment, PasteFile

from rest_framework.response import Response
from rest_framework import status
import json


class Index(CreateView):
    model = PasteFile
    form_class = PasteForm


class Detail(DetailView):
    template_name = "paste/detail.html"
    model = PasteFile

    def get(self, request, slug):
        paste_obj = get_object_or_404(PasteFile, slug=slug)
        context = dict(
            object=paste_obj,
            comments=Comment.objects.filter(paste_file__id=paste_obj.id),
            form=CommentForm(),
            slug=slug,
        )
        return render(request, self.template_name, context)

    def post(self, request, slug):
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                post = get_object_or_404(PasteFile, slug=slug)
                comment = form.save(commit=False)
                comment.paste_file = post
                comment.slug = post.slug
                comment.save()
                return redirect(post.get_absolute_url())
        return render(request, self.template_name, paste_content)


class CommentThread(CreateView):
    template_name = "paste/comment_thread.html"
    form_class = CommentForm
    http_method_names = ["get", "post"]

    def form_valid(self, form):
        self.parent_comment = self.get_parent_comment()
        form = form.save(commit=False)
        form.paste_file = self.parent_comment.paste_file
        form.parent = self.parent_comment
        form.slug = self.parent_comment.slug
        return super().form_valid(form)

    def get_parent_comment(self):
        return get_object_or_404(Comment, id=self.kwargs.get("id"))

    def get_success_url(self):
        return reverse("paste:detail", kwargs={"slug": self.parent_comment.slug})


class RawContent(DetailView):
    model = PasteFile

    def get(self, request, slug):
        paste_obj = get_object_or_404(PasteFile, slug=slug)
        context = paste_obj.content
        return HttpResponse(context, content_type="text/plain; charset=utf8")


class AllPastes(DetailView):
    def get(self, request):
        pastes = PasteFile.objects.all()
        pastes_list = []
        for paste in pastes:
            paste_dict = {}
            paste_dict['title'] = paste.title
            paste_dict['content'] = paste.content
            paste_dict['url'] = request.build_absolute_uri(paste.get_absolute_url())
            paste_dict['date_time'] = paste.date_time.strftime('%Y-%m-%dT%H:%M:%S.%f')
            pastes_list.append(paste_dict)
        return HttpResponse(json.dumps(pastes_list), content_type="application/json")

