import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from utilities.mixins import ResponseViewMixin
from vendors.serializers import  VendorsSerializers
from vendors.models import Vendors
import uuid


class Vendor(APIView, ResponseViewMixin):
    def post(self, request):
        try:
            serializer = VendorsSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save(vendor_code = str(uuid.uuid4())[:10])
                return ResponseViewMixin.success_response(code="HTTP_200_OK", message="Vendor added successfully!", data="")
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message=serializer.error_messages, data= "")

        except Exception as e:
            print(str(e))
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message=str(e), data= "")

    def get(self, request, *args, **kwargs):
        try:
            vendor_id = kwargs.get('vendor_id')
            if vendor_id:
                vendor = Vendors.objects.get(id=vendor_id)
                data = {
                    "name": vendor.name,
                    "contact_details": vendor.contact_number,
                    "address" : vendor.address,
                    "vendor_code" : vendor.vendor_code
                }

                return ResponseViewMixin.success_response(code="HTTP_200_OK", message="Vendor Found!", data = data)
            else:
                res = []
                vendors = Vendors.objects.all()
                for v in vendors:
                    data = {
                        "name": v.name,
                        "contact_details": v.contact_number,
                        "address" : v.address,
                        "vendor_code" : v.vendor_code
                    }
                    res.append(data)
                return ResponseViewMixin.success_response(code="HTTP_200_OK", message="All vendors detail.", data = res)
        except Vendors.DoesNotExist:
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="Vendor not found with this ID!", data= "")
        except Exception as e:
            print(str(e))
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message=str(e), data= "")


    def put(self, request, vendor_id):
        try:
            vendor = Vendors.objects.get(id=vendor_id)
            if vendor:
                serializer = VendorsSerializers(vendor, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return ResponseViewMixin.success_response(code="HTTP_200_OK", message="Vendor updated successfully!.", data = '')
                else:
                    return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message=serializer.error_messages, data= "")
        except Vendors.DoesNotExist:
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="Vendor not found with this ID!", data= "")

        except Exception as e:
            print(str(e))
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="Something went wrong!", data= "")


    def delete(self, request, vendor_id):
        try:
            vendor = Vendors.objects.get(id=vendor_id).delete()
            if vendor:
                return ResponseViewMixin.success_response(code="HTTP_200_OK", message="Vendor deleted successfully!.", data = '')
        except Vendors.DoesNotExist:
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="Vendor not found with this ID!", data= "")

        except Exception as e:
            print(str(e))
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="Something went wrong!", data= "")


class Vendor_Performance_Metrics(APIView, ResponseViewMixin):
    def get(self, request, vendor_id):
        try:
            vendor = Vendors.objects.get(id=vendor_id)
            if vendor:
                data = {
                    "name":vendor.name,
                    "contact_number": vendor.contact_number,
                    "address":vendor.address,
                    "vendor_code" : vendor.vendor_code,
                    "on_time_delivery_rate":(str(vendor.on_time_delivery_rate) + " %") if vendor.on_time_delivery_rate != None else '',
                    "quality_rating_avg":vendor.quality_rating_avg,
                    "average_response_time": (str(vendor.average_response_time) + " days") if vendor.average_response_time != None else '',
                    "fulfillment_rate": (str(vendor.fulfillment_rate) + " %") if vendor.fulfillment_rate != None else ''
                }
                return ResponseViewMixin.success_response(code="HTTP_200_OK", message="Vendor performance metrics!.", data = data)
        except Vendors.DoesNotExist:
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="Vendor not found with this ID!", data= "")

        except Exception as e:
            print(str(e))
            return ResponseViewMixin.error_response(code="HTTP_400_BAD_REQUEST", message="Something went wrong!", data= "")

