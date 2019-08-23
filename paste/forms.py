from django import forms
from django.forms import ModelForm

from .models import PasteFile


class PasteForm(ModelForm):
    content = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": 15, "cols": 80})
    )

    class Meta:
        model = PasteFile
        fields = ("title", "content")
