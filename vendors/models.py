from django.db import models

# Create your models here.




class Vendors(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    contact_number = models.CharField(max_length=10, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    vendor_code = models.CharField(max_length=50, blank=False, null=False)
    on_time_delivery_rate = models.FloatField(blank=True, null=True)
    quality_rating_avg = models.FloatField(blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    fulfillment_rate = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name





