from django.http import HttpRequest, HttpResponse

from rest_framework import views, generics
from rest_framework.request import Request as RestRequest
from rest_framework.response import Response as RestResponse

import requests

from .serializers import *


class DataView(views.APIView):
    def get(self, request: RestRequest) -> RestResponse:
        origin = request.META.get('HTTP_ORIGIN', 'localhost:3000').split('/')[
            -1]
        print(origin)

        try:
            settings = SiteSettings.objects.get(url=origin)
        except SiteSettings.DoesNotExist:
            return RestResponse(status=401, exception=True)

        return RestResponse(SiteSettingSerializer(settings).data)


def validate_ticket(request: HttpRequest):
    print(request.GET)
    ticket = request.GET['ticket']
    d = requests.get('https://accounts.esn.org/cas/serviceValidate', params={
        'service': 'https%3A//esnrussia-web-backend.herokuapp.com/validate_ticket/',
        'ticket': ticket
    })
    print(d.url)
    return HttpResponse(d.content)
