from rest_framework import generics, permissions, serializers, status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, CompanySerializer, DriverSerializer, \
    CompanyDriverSerializer
from django.contrib.auth import login, authenticate
from knox.views import LoginView as KnoxLoginView
import base64
from .models import Driver, Company, Company3ver


# User Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


# Driver Register API
class DriverRegisterAPI(generics.GenericAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        # Получение и кодирование файлов в формат base64
        driver_license_file = request.FILES.get('driver_license')
        straxovka_file = request.FILES.get('straxovka')

        if driver_license_file:
            data['driver_license'] = self.encode_file_to_base64(driver_license_file)

        if straxovka_file:
            data['straxovka'] = self.encode_file_to_base64(straxovka_file)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        driver = serializer.save()
        return Response({
            "driver": DriverSerializer(driver, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(driver.user)[1]
        })

    def encode_file_to_base64(self, file):
        try:
            file_data = file.read()
            encoded_data = base64.b64encode(file_data)
            return encoded_data.decode('utf-8')
        except Exception as e:
            raise serializers.ValidationError("Ошибка при кодировании файла")


# Company Register API
class CompanyRegisterAPI(generics.GenericAPIView):
    serializer_class = CompanySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = serializer.save()
        return Response({
            "company": CompanySerializer(company, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(company.user)[1]
        })


# Company Driver Register API
class CompanyDriverRegisterAPI(generics.GenericAPIView):
    serializer_class = CompanyDriverSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company_driver = serializer.save()
        return Response({
            "driver": CompanyDriverSerializer(company_driver, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(company_driver.user)[1]
        })


# ------------------------------------------------------------------------------------
# User Profile API
class UserProfileAPI(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# Company Profile API
class CompanyDetailAPI(generics.RetrieveUpdateAPIView):
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def get_object(self):
        return self.request.user.company

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)


# Company Driver Profile API
class CompanyDriverDetailAPI(generics.RetrieveUpdateAPIView):
    serializer_class = CompanyDriverSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        company_driver = self.get_object()
        serializer = CompanyDriverSerializer(company_driver)
        return Response(serializer.data)

    def get_object(self):
        return Company3ver.objects.get(user=self.request.user)

    def get_queryset(self):
        return Company3ver.objects.filter(user=self.request.user)


# Driver Profile API
class DriverDetailAPI(generics.RetrieveUpdateAPIView):
    serializer_class = DriverSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        driver = self.get_object()
        serializer = DriverSerializer(driver)
        return Response(serializer.data)

    def get_object(self):
        return self.request.user.driver

    def get_queryset(self):
        return Driver.objects.filter(user=self.request.user)


# ------------------------------------------------------------------------

# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            serialized_user = UserSerializer(user)
            return Response({
                "user": serialized_user.data,
                "token": AuthToken.objects.create(user)[1]
            })
        else:
            return Response({
                "error": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)
