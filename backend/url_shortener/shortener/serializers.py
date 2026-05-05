from rest_framework.serializers import ModelSerializer
from .models import Url


class UrlSerializer(ModelSerializer):
    class Meta:
        model = Url
        fields = ["id", "main_link", "short_link", "last_accessed"]
