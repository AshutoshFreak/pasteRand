import uuid

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now


class PasteFile(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("paste:detail", kwargs={"slug": self.slug})

    def get_slug(self):
        uuid_value = str(uuid.uuid4())
        unique_slug = slugify(uuid_value[0:13])
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        return super(PasteFile, self).save(*args, **kwargs)


class Comment(models.Model):
    paste_file = models.ForeignKey(
        "paste.PasteFile", on_delete=models.CASCADE, related_name="comments", null=True
    )
    comment_text = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    comment_id = models.AutoField(primary_key=True)
    slug = models.SlugField()

    def __str__(self):
        return self.comment_text

    # replies
    def children(self):
        return self.__class__.objects.filter(parent=self)
