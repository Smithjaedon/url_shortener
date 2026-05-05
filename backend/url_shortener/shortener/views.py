from django.shortcuts import redirect
from rest_framework import viewsets
from .serializers import UrlSerializer
from .models import Url
from rest_framework.decorators import action
from rest_framework.response import Response

import secrets


# Create your views here.
class UrlViewSet(viewsets.ModelViewSet):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer

    @action(detail=False, methods=["post"], url_path="shorten")
    def shorted(self, request):
        link = request.data.get("link")
        if not link:
            return Response({"status": 404})

        code = secrets.token_urlsafe(8)
        Url.objects.create(main_link=link, short_link=code)
        return Response({"short_link": code})

    @action(detail=False, methods=["get"], url_path="(?P<code>[^/.]+)")
    def use_redirect(self, request, code=None):
        short_url = Url.objects.get(short_link=code)
        short_url.save()
        return Response({"redirect_link": short_url.main_link})
