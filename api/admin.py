from django.contrib import admin

from .models import SiteSettings, Page

admin.site.register(SiteSettings)
admin.site.register(Page)
