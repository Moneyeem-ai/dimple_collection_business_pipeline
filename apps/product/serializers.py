from rest_framework import serializers
from .models import PTFileEntry


class PTFileEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PTFileEntry
        fields = '__all__'
        depth = 1


class PTFileEntryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PTFileEntry
        fields = '__all__'
