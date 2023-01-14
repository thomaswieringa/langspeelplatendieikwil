from rest_framework import serializers

from .models import Master


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = ["master_id", "title", "artist", "genre", "year", "discogs_url", "image_url"]