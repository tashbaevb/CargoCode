from django.urls import path

from .views import ReviewView

urlpatterns = [
    path("", ReviewView.as_view(), name="review_list"),
]
