from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, permissions

from .models import Review
from .serializers import ReviewSerializer


class ReviewView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

