from django.contrib import admin

from .models import SiteSettings, Page, EsnAuthToken

admin.site.register(SiteSettings)
admin.site.register(Page)
admin.site.register(EsnAuthToken)
