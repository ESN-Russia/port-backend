import datetime as dt

from django.db import models


class SiteSettings(models.Model):
    url = models.CharField(primary_key=True, max_length=250, null=False)
    maintenance = models.BooleanField(null=False)
    logo_url = models.CharField(max_length=250)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.url


class Page(models.Model):
    site = models.ForeignKey(to=SiteSettings, related_name='pages',
                             on_delete=models.DO_NOTHING)
    url = models.CharField(primary_key=True, max_length=250, null=False)
    title = models.CharField(max_length=255)
    page_data = models.TextField(null=False, default='')

    def __str__(self):
        return f'[{self.site}{self.url}] {self.title}'


class EsnAuthToken(models.Model):
    nanoid = models.CharField(max_length=32, primary_key=True)
    url = models.CharField(max_length=255, null=False)
    username = models.CharField(max_length=255)
    expire_at = models.DateTimeField(
        default=dt.datetime.now() + dt.timedelta(days=1))

    def __str__(self):
        return f'{self.username} vs {self.url}'