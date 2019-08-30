from django.contrib import admin

from .models import Comment, PasteFile

admin.site.register(PasteFile)
admin.site.register(Comment)
