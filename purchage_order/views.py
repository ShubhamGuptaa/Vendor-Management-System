

from purchage_order.serializers import PurchageOrderSerializer
from rest_framework.views import APIView
from utilities.mixins import ResponseViewMixin
import uuid
import datetime
from vendors.models import Vendors
from vendors.serializers import VendorsSerializers
from purchage_order.models import Purchage_Order
import pytz
# Create your views here.

class Purchage_Orders(APIView, ResponseViewMixin):
    def post(self, request):
        try:
            vendor_id = request.data.get('vendor_id')
            if vendor_id:
                vendor = Vendors.objects.get(id=vendor_id)
                if vendor:
                    serializer = PurchageOrderSerializer(data=request.data)
                    print(serializer)
                    if serializer.is_valid():
                        po_number = str(uuid.uuid4())[:12]
                        order_date = datetime.datetime.now()
                        delivery_date = order_date + datetime.timedelta(days=4)
                        quantity = len(serializer.validated_data.get('items', []))
                        issue_date = datetime.datetime.now()
                        serializer.save(vendor=vendor, po_number = po_number, order_date = order_date, delivery_date = delivery_date, quantity = quantity, issue_date = issue_date)
                        return ResponseViewMixin.success_response(code="HTTP_200_OK", message=f"Your order with po_number:'{po_number}'created successfully and is expected to deliver on {delivery_date}", data = '')
                else:
                    return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message=serializer.error_messages, data= "")
            else:
                return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="Vendor ID is missing!", data= "")
        except Vendors.DoesNotExist:
            return ResponseViewMixin.error_response(code="HTTP_404_NOT_FOUND", message="Vendor Doesnot Exisit with this ID", data= "")

        except Exception as e:
            print(str(e))
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="Something went wrong!", data= "")


    def get(self, request, *args, **kwargs):
        try:
            vendor_id = request.query_params['filter_by'] if request.query_params and 'filter_by' in request.query_params else None
            res = []
            po_id = kwargs.get('po_id')
            if po_id:
                purchage_orders = Purchage_Order.objects.get(id=po_id)
                if purchage_orders:
                    serializer = PurchageOrderSerializer(purchage_orders)
                    data = {
                        'po_number': serializer.data['po_number'],
                        'items': serializer.data['items'],
                        'order_date': serializer.data['order_date'],
                        'delivery_date': serializer.data['delivery_date'],
                        'quantity': serializer.data['quantity'],
                        'status': serializer.data['status'],
                        'vendor': serializer.data['vendor']
                        }
                    return ResponseViewMixin.success_response(code="HTTP_200_OK", message=f"List of all the purchage orders!", data = data)
            if vendor_id != None:
                purchage_orders = Purchage_Order.objects.filter(vendor_id=vendor_id)
                for p in purchage_orders:
                    serializer = PurchageOrderSerializer(p)
                    data = {
                    'po_number': serializer.data['po_number'],
                    'items': serializer.data['items'],
                    'order_date': serializer.data['order_date'],
                    'delivery_date': serializer.data['delivery_date'],
                    'quantity': serializer.data['quantity'],
                    'status': serializer.data['status'],
                    'vendor': serializer.data['vendor']
                    }
                    res.append(data)
                return ResponseViewMixin.success_response(code="HTTP_200_OK", message=f"List of all the purchage orders!", data = res)
            else:
                purchage_orders = purchage_orders = Purchage_Order.objects.all()
                for p in purchage_orders:
                    serializer = PurchageOrderSerializer(p)
                    print(serializer.data)
                    data = {
                    'po_number': serializer.data['po_number'],
                    'items': serializer.data['items'],
                    'order_date': serializer.data['order_date'],
                    'delivery_date': serializer.data['delivery_date'],
                    'quantity': serializer.data['quantity'],
                    'status': serializer.data['status'],
                    'vendor': serializer.data['vendor']
                    }
                    res.append(data)
                return ResponseViewMixin.success_response(code="HTTP_200_OK", message=f"List of all the purchage orders!", data = res)
        except Exception as e:
            print(str(e))
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="Something went wrong!", data= "")


    def put(self, request, po_id):
        try:
            po = Purchage_Order.objects.get(id=po_id)
            if po:
                serializer = PurchageOrderSerializer(po, data=request.data)
                if serializer.is_valid():
                    serializer.save(acknowledgment_date=datetime.datetime.now())
                    return ResponseViewMixin.success_response(code="HTTP_200_OK", message="purchage order updated successfully!.", data = '')
                else:
                    return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message=serializer.error_messages, data= "")
        except Purchage_Order.DoesNotExist:
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="po not found with this ID!", data= "")

        except Exception as e:
            print(str(e))
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="Something went wrong!", data= "")


    def delete(self, request, po_id):
        try:
            po = Purchage_Order.objects.get(id=po_id).delete()
            if po:
                return ResponseViewMixin.success_response(code="HTTP_200_OK", message="purchage order deleted successfully!.", data = '')
            
        except Purchage_Order.DoesNotExist:
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="po not found with this ID!", data= "")

        except Exception as e:
            print(str(e))
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="Something went wrong!", data= "")


class AcknowledgementPOs(APIView, ResponseViewMixin):
    def post(self, request, po_id):
        try:
            if po_id:
                po = Purchage_Order.objects.get(id=po_id)
                if po:
                    if not po.acknowledgment_date:
                        po.acknowledgment_date = datetime.datetime.now(pytz.UTC)
                        time_diff = po.acknowledgment_date - po.issue_date
                        po.vendor.average_response_time = time_diff.days
                        po.vendor.save()
                        po.save()
                        return ResponseViewMixin.success_response(code="HTTP_200_OK", message="Acknowledged successfully!.", data = '')
                    else:
                        prev_acknowledge_date = po.acknowledgment_date
                        po.acknowledgment_date = datetime.datetime.now(pytz.UTC)
                        time_diff = po.acknowledgment_date - prev_acknowledge_date
                        po.vendor.average_response_time = time_diff.days
                        po.vendor.save()
                        po.save()
                        return ResponseViewMixin.success_response(code="HTTP_200_OK", message="Acknowledged successfully!.", data = '')
            else:
                return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="please provide the po ID!.", data = '')
        except  Purchage_Order.DoesNotExist:
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="Given po ID doesnot exisit!", data= "")

        except Exception as e:
            print(str(e))
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="Something went wrong!", data= "")



