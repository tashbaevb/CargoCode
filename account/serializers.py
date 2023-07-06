import base64
from rest_framework import serializers
from .models import Driver, Company, Company3ver, Profile
from django.contrib.auth.models import User
from django.core.files.base import ContentFile


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# Driver Serializer
class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Driver
        fields = (
            'id', 'user', 'driver_license', 'straxovka', 'car_number',
            'car_title', 'car_year', 'car_type', 'bank', 'name', 'phone_number'
        )

    # Create data
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        email = user_data['email']
        password = user_data['password']

        user = User.objects.create_user(email=email, username=email)
        user.set_password(password)
        user.save()

        driver_license_file = validated_data.pop('driver_license')
        straxovka_file = validated_data.pop('straxovka')

        driver_license_data = base64.b64decode(driver_license_file)
        straxovka_data = base64.b64decode(straxovka_file)

        driver_license = ContentFile(driver_license_data, name='driver_license')
        straxovka = ContentFile(straxovka_data, name='straxovka')

        driver = Driver.objects.create(user=user, driver_license=driver_license, straxovka=straxovka, **validated_data)
        return driver

    # Update data
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = self.fields['user']
            user = instance.user
            user = user_serializer.update(user, user_data)
            validated_data['user'] = user
        return super().update(instance, validated_data)

    # Read data
    def retrieve(self, instance):
        user_serializer = self.fields['user']
        user_data = user_serializer.to_representation(instance.user)
        ret = super().retrieve(instance)
        ret.data['user'] = user_data
        return ret


# Company Serializer
class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Company
        fields = ('id', 'user', 'company_name', 'dot_number', 'descriptions', 'bank_account')

    # Create data
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        email = user_data['email']
        password = user_data['password']
        user = User.objects.create_user(email=email, username=email)
        user.set_password(password)
        user.save()
        company = Company.objects.create(user=user, **validated_data)
        return company

    # Update data
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = self.fields['user']
            user = instance.user
            user = user_serializer.update(user, user_data)
            validated_data['user'] = user
        return super().update(instance, validated_data)

    # Read data
    def retrieve(self, instance):
        user_serializer = self.fields['user']
        user_data = user_serializer.to_representation(instance.user)
        ret = super().retrieve(instance)
        ret.data['user'] = user_data
        return ret


# Company Driver Serializer
class CompanyDriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Company3ver
        fields = ('id', 'user', 'car_number', 'car_type', 'car_title')

    # Create data
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        email = user_data['email']
        password = user_data['password']
        user = User.objects.create_user(email=email, username=email)
        user.set_password(password)
        user.save()
        company_driver = Company3ver.objects.create(user=user, **validated_data)
        return company_driver

    # Update data
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = self.fields['user']
            user = instance.user
            user = user_serializer.update(user, user_data)
            validated_data['user'] = user
        return super().update(instance, validated_data)

    # Read data
    def retrieve(self, instance):
        user_serializer = self.fields['user']
        user_data = user_serializer.to_representation(instance.user)
        ret = super().retrieve(instance)
        ret.data['user'] = user_data
        return ret


# ------------------------------------------------------------------------------------

# User Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    # Create user
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'],
            validated_data['email'],
            validated_data['password']
        )
        return user
