# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from purchage_order.models import Purchage_Order
from vendors.models import Vendors
from django.db import transaction
from historical_performance.models import Historical_Performance
from django.db.models import Count, F, ExpressionWrapper, fields
from django.db.models import Sum

@receiver(post_save, sender=Purchage_Order)
def update_vendor_metrics_on_po_save(sender, instance, created, **kwargs):
    if not created:
        update_vendor_metrics(instance.vendor)



@receiver(post_delete, sender=Purchage_Order)
def update_vendor_metrics_on_po_delete(sender, instance, **kwargs):
    update_vendor_metrics(instance.vendor)



@receiver(post_save, sender=Vendors)
def create_vendor_performance_record(sender, instance, created, **kwargs):
    if created:
        Historical_Performance.objects.create(
            vendor=instance,
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0,
        )


@transaction.atomic
def update_vendor_metrics(vendor):
    completed_orders = Purchage_Order.objects.filter(vendor=vendor, status=1)
    total_orders = Purchage_Order.objects.filter(vendor=vendor)
    on_time_delivery_rate = calculate_on_time_delivery_rate(completed_orders)
    quality_rating_avg = calculate_quality_rating_avg(completed_orders)
    average_response_time = (calculate_average_response_time(completed_orders)).days
    fulfillment_rate = calculate_fulfillment_rate(total_orders)

    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.quality_rating_avg = quality_rating_avg
    vendor.average_response_time = average_response_time
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()

def calculate_on_time_delivery_rate(orders):
    total_completed_orders = len(orders)
    on_time_completed_orders = len(orders.filter(delivery_date__lte=F('acknowledgment_date')))
    on_time_delivery_rate = (on_time_completed_orders / total_completed_orders) * 100 if total_completed_orders > 0 else 0.0
    return on_time_delivery_rate


def calculate_quality_rating_avg(orders):
    completed_orders = orders.exclude(quality_rating__isnull=True)

    total_quality_rating = completed_orders.aggregate(Sum('quality_rating'))['quality_rating__sum']
    total_completed_orders = len(orders)

    if total_completed_orders > 0:
        quality_rating_avg = total_quality_rating / total_completed_orders
    else:
        quality_rating_avg = 0.0

    return quality_rating_avg

def calculate_average_response_time(orders):
    acknowledged_orders = orders.exclude(acknowledgment_date__isnull=True)
    total_response_time = acknowledged_orders.annotate(
        response_time=ExpressionWrapper(
            F('acknowledgment_date') - F('issue_date'),
            output_field=fields.DurationField()
        )
    ).aggregate(Sum('response_time'))['response_time__sum']

    total_acknowledged_orders = acknowledged_orders.count()

    if total_acknowledged_orders > 0:
        average_response_time = total_response_time / total_acknowledged_orders
    else:
        average_response_time = 0.0

    return average_response_time

def calculate_fulfillment_rate(orders):
    total_orders = len(orders)
    if total_orders == 0:
        return 0.0

    fulfilled_orders = orders.filter(status=1)
    fulfilled_count = fulfilled_orders.count()

    fulfillment_rate = (fulfilled_count / total_orders) * 100.0

    return fulfillment_rate

