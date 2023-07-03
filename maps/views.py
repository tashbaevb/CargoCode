from django.shortcuts import render
from rest_framework import permissions,authentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

# Create your views here.

class MapView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        return Response({"ok":"ok"})
