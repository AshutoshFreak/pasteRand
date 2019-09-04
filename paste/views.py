from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView

from .forms import CommentForm, PasteForm
from .models import Comment, PasteFile


class Index(CreateView):
    model = PasteFile
    form_class = PasteForm

    def form_valid(self, form):
        instance = form.save()
        return redirect(instance.get_absolute_url())


class Detail(DetailView):
    template_name = "paste/detail.html"
    model = PasteFile

    def get(self, request, slug):
        paste_obj = get_object_or_404(PasteFile, slug=slug)
        comments = Comment.objects.filter(paste_file_id=paste_obj.pk, parent=None)

        form = CommentForm()
        paste_content = {
            "title": paste_obj.title,
            "content": paste_obj.content,
            "date_time": paste_obj.date_time,
            "pk": paste_obj.pk,
            "comments": comments,
            "form": form,
        }
        return render(request, self.template_name, paste_content)

    def post(self, request, slug):
        post = get_object_or_404(PasteFile, slug=slug)
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save()
                comment.paste_file = post
                comment.slug = post.slug
                comment.save()
                return redirect(post.get_absolute_url())
        return render(request, self.template_name, paste_content)


def comment_thread(request, id):
    parent_comment = get_object_or_404(Comment, comment_id=id)
    post = get_object_or_404(PasteFile, slug=parent_comment.slug)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            comment.paste_file = parent_comment.paste_file
            comment.parent = parent_comment
            comment.slug = parent_comment.slug
            comment.save()
            return redirect(post.get_absolute_url())
    return render(request, "paste/comment_thread.html", {"form": form})
