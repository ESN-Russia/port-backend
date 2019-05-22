from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from rest_framework import views, generics
from rest_framework.request import Request as RestRequest
from rest_framework.response import Response as RestResponse

import requests
import json

from .serializers import *


class DataView(views.APIView):
    def get(self, request: RestRequest) -> RestResponse:
        token_id = request.META.get('X-AUTH', '_')
        origin = request.META.get('HTTP_ORIGIN', 'localhost:3000').split('/')[
            -1]
        try:
            token = EsnAuthToken.objects.get(nanoid=token_id)
            if token.url != origin or not token.username:
                return RestResponse(status=401, exception=True)
        except EsnAuthToken.DoesNotExist:
            return RestResponse(status=401, exception=True)

        try:
            settings = SiteSettings.objects.get(url=origin)
        except SiteSettings.DoesNotExist:
            return RestResponse(status=401, exception=True)

        return RestResponse(SiteSettingSerializer(settings).data)


CAS_SERVER = 'https://accounts.esn.org/cas'
CAS_CALLBACK = 'https://esnrussia-web-backend.herokuapp.com/validate_ticket'


def validate_ticket(request: HttpRequest, token_id):
    ticket = request.GET['ticket']
    d = requests.get(f'{CAS_SERVER}/serviceValidate', params={
        'service': f'{CAS_CALLBACK}/{token_id}/',
        'ticket': ticket
    })
    username = d.text.split()[0]
    token = EsnAuthToken.objects.get(nanoid=token_id)
    token.username = username
    token.save()

    return HttpResponseRedirect(redirect_to=f'https://{token.url}')


def login_redirect(req: HttpRequest):
    try:
        token_id = req.GET['token']
        url = req.GET['frontend']
    except ValueError:
        return HttpResponse(status=400)

    token = EsnAuthToken.objects.create(nanoid=token_id, url=url)
    token.save()

    return HttpResponseRedirect(
        redirect_to=f'{CAS_SERVER}/login?service={CAS_CALLBACK}/{token_id}/')
