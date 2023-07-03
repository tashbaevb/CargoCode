from django.urls import path
from knox import views as knox_views

from .views import (CompanyDriverRegisterAPI, CompanyRegisterAPI,
                    DriverRegisterAPI, LoginAPI, RegisterAPI)

urlpatterns = [
    path("api/register/", RegisterAPI.as_view(), name="register"),
    path("api/driver/register/", DriverRegisterAPI.as_view(), name="driver_register"),
    path(
        "api/company/register/", CompanyRegisterAPI.as_view(), name="company_register"
    ),
    path(
        "api/company/driver/register/",
        CompanyDriverRegisterAPI.as_view(),
        name="company_driver_register",
    ),
    path("api/login/", LoginAPI.as_view(), name="login"),
    path("api/logout/", knox_views.LogoutView.as_view(), name="logout"),
    path("api/logoutall/", knox_views.LogoutAllView.as_view(), name="logoutall"),
]
