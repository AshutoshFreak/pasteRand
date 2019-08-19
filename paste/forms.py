from django.forms import ModelForm

from .models import PasteFile


class PasteForm(ModelForm):
    class Meta:
        model = PasteFile
        fields = ("title", "content")
