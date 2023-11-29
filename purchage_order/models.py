from django.db import models
from vendors.models import Vendors
from utilities.constants import Konstants, Kw

# Create your models here.
STATUS = Konstants(
    Kw(pending=0, label='Pending'),
    Kw(completed=1, label='Completed'),
    Kw(canceled=2, label='Canceled')
)

class Purchage_Order(models.Model):
    po_number = models.CharField(max_length=100)
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField(default=dict)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50,choices=STATUS.choices(), default=STATUS.pending)
    quality_rating = models.FloatField(blank=True, null=True)
    issue_date = models.DateTimeField(blank=False, null=False)
    acknowledgment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.po_number