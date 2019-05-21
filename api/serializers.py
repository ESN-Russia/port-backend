from rest_framework import serializers
from .models import *


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['url', 'title', 'page_data']


class SiteSettingSerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True)

    class Meta:
        model = SiteSettings
        fields = ['name', 'logo_url', 'maintenance', 'pages']
