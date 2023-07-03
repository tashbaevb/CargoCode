from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, CompanySerializer, DriverSerializer, \
    CompanyDriverSerializer
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
import base64
from django.core.files.base import ContentFile
from .models import Driver


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


# ------------------------------------------------------------------------

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


# Login API
# class LoginAPI(generics.GenericAPIView):
#     serializer_class = AuthTokenSerializer
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request, format=None):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(request, email=email, password=password)
#
#         if user:
#             login(request, user)
#             return super(LoginAPI, self).post(request, format=None)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super(LoginAPI, self).post(request, format=None)
