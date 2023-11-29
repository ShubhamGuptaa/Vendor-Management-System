from django.db import models

from vendors.models import Vendors

# Create your models here.

class Historical_Performance(models.Model):
    vendor = models.ForeignKey(Vendors, related_name='vendor', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(blank=False, null=False)
    quality_rating_avg = models.FloatField(blank=False, null=False)
    average_response_time =  models.FloatField(blank=False, null=False)
    fulfillment_rate = models.FloatField(blank=False, null=False)
