import base64

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Company, Company3ver, Driver


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}


# Driver Serializer
class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = (
            "id",
            "user",
            "driver_license",
            "straxovka",
            "car_number",
            "car_title",
            "car_year",
            "car_type",
            "bank",
        )

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        email = user_data["email"]
        password = user_data["password"]

        user = User.objects.create_user(email=email, username=email)
        user.set_password(password)
        user.save()

        driver_license_file = validated_data.pop("driver_license")
        straxovka_file = validated_data.pop("straxovka")

        driver_license_data = base64.b64decode(driver_license_file)
        straxovka_data = base64.b64decode(straxovka_file)

        driver_license = ContentFile(driver_license_data, name="driver_license")
        straxovka = ContentFile(straxovka_data, name="straxovka")

        driver = Driver.objects.create(
            user=user,
            driver_license=driver_license,
            straxovka=straxovka,
            **validated_data
        )
        return driver


# Company Serializer
class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Company
        fields = (
            "id",
            "user",
            "company_name",
            "dot_number",
            "descriptions",
            "bank_account",
        )

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        email = user_data["email"]
        password = user_data["password"]

        user = User.objects.create_user(email=email, username=email)
        user.set_password(password)
        user.save()

        company = Company.objects.create(user=user, **validated_data)
        return company


# Company Driver Serializer
class CompanyDriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Company3ver
        fields = ("id", "user", "car_number", "car_type", "car_title")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        email = user_data["email"]
        password = user_data["password"]

        user = User.objects.create_user(email=email, username=email)
        user.set_password(password)
        user.save()

        company_driver = Company3ver.objects.create(user=user, **validated_data)
        return company_driver


# ------------------------------------------------------------------------------------


# User Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"], validated_data["email"], validated_data["password"]
        )
        return user


# Register Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             validated_data['username'],
#             validated_data['email'],
#             validated_data['password']
#         )
#         user.role = 'user'
#         user.save()
#         return user
