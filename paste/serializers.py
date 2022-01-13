from rest_framework import serializers
from .models import PasteFile

class PasteFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasteFile
        fields = '__all__'
        