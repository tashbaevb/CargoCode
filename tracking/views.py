from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from account import models as acc_models
from .models import Coordinate, Device
from .serializers import CoordinateSerializer, DeviceSerializer


class DeviceListView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        List all the device items for given requested user
        """
        driver = acc_models.Driver.objects.get(user_id=request.user.id)
        devices = Device.objects.filter(user=driver.id)
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create the device with given url data
        """
        data = request.data
        driver = acc_models.Driver.objects.get(user_id=request.user.id)
        data.update({"user": driver.id})
        serializer = DeviceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceDetailView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, token, user_id):
        """
        Helper method to get the object with given url_id, and user_id
        """
        try:
            return Device.objects.get(token=token, user=user_id)
        except Device.DoesNotExist:
            return None

    def post(self, request, token, *args, **kwargs):
        """
        Updates the device item with given token if exists
        """
        driver = acc_models.Driver.objects.get(user_id=request.user.id)
        device_instance = self.get_object(token, driver.id)
        if not device_instance:
            return Response(
                {"detail": "Object with device token does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        data = request.data
        data.update({"user": driver.id})
        serializer = DeviceSerializer(instance=device_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, token, *args, **kwargs):
        """
        Retrieves the Url with given url_id
        """
        driver = acc_models.Driver.objects.get(user_id=request.user.id)
        device_instance = self.get_object(token, driver.id)
        if not device_instance:
            return Response(
                {"detail": "Object with url id does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = DeviceSerializer(device_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, token, *args, **kwargs):
        """
        Deletes the url item with given url_id if exists
        """
        driver = acc_models.Driver.objects.get(user_id=request.user.id)
        device_instance = self.get_object(token, driver.id)
        if not device_instance:
            return Response(
                {"detail": "Object with url id does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        device_instance.delete()
        return Response({"detail": "Object deleted!"}, status=status.HTTP_200_OK)


class CoordinateListView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_device_obj(self, token, user_id):
        """
        Helper method to get the object with given url_id, and user_id
        """
        try:
            return Device.objects.get(token=token, user=user_id)
        except Device.DoesNotExist:
            return None

    def get(self, request, token, *args, **kwargs):
        """
        List all the coordinate items for given requested user
        """
        driver = acc_models.Driver.objects.get(user_id=request.user.id)
        device = self.get_device_obj(token, driver.id)
        coordinates = Coordinate.objects.filter(device=device.id)[:20]
        serializer = CoordinateSerializer(coordinates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, token, *args, **kwargs):
        """
        Create the coordinate with given token data
        """
        driver = acc_models.Driver.objects.get(user_id=request.user.id)
        device_instance = self.get_device_obj(token, driver.id)
        if not device_instance:
            return Response(
                {"detail": "Object with device token does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        data = request.data
        data.update({"device": device_instance.id})
        serializer = CoordinateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoordinateCurrentView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_device_obj(self, token, user_id):
        """
        Helper method to get the object with given url_id, and user_id
        """
        try:
            return Device.objects.get(token=token, user=user_id)
        except Device.DoesNotExist:
            return None

    def get(self, request, token, *args, **kwargs):
        """
        List all the url items for given requested user
        """
        driver = acc_models.Driver.objects.get(user_id=request.user.id)
        device_instance = self.get_device_obj(token, driver.id)
        if not device_instance:
            return Response(
                {"detail": "Object with device token does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        coordinate = Coordinate.objects.filter(device=device_instance.id).latest(
            "created_date"
        )
        serializer = CoordinateSerializer(coordinate, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CoordinateGetView(APIView):
    def get_device_obj(self, token):
        """
        Helper method to get the object with given url_id, and user_id
        """
        try:
            return Device.objects.get(token=token)
        except Device.DoesNotExist:
            return None

    def get(self, request, token, *args, **kwargs):
        device_instance = self.get_device_obj(token)
        if not device_instance:
            return Response(
                {"detail": "Object with device token does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        latitude = self.request.data['lat']
        longitude = self.request.data['lon']
        data = {"lat": latitude, "lon": longitude, "device": device_instance.id}
        serializer = CoordinateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
