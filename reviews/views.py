from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, permissions

from .models import Review
from .serializers import ReviewSerializer


class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# old
# class ReviewCreate(generics.CreateAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer


class ReviewCreate(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        data = self.request.data
        username = data.pop("email")
        User = get_user_model(username)
        participant = User.objects.get(username=username)
        serializer.save(user=self.request.user)
