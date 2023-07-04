from django.urls import path

from .views import ReviewCreate, ReviewList

urlpatterns = [
    path("", ReviewList.as_view(), name="review_list"),
    path("new/", ReviewCreate.as_view(), name="review_create"),
]
