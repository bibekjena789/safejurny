from django.db import models
import os
from django.utils.text import slugify
from django.db import models





class AdminIP(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    server_time = models.DateTimeField(auto_now=True)
    activity= models.TextField(blank=True, null=True)
    local_time = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.ip_address} - {self.activity} @ {self.timestamp}"