from django.shortcuts import render
from utilities.mixins import ResponseViewMixin
from rest_framework.views import APIView
# Create your views here.

class Historical_Performance(APIView, ResponseViewMixin):
    def post(self, request, *args,):
        pass