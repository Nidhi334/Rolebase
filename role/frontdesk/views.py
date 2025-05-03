from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(
            {"message": "Doctor updated successfully"},
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Doctor deleted successfully"},
            status=status.HTTP_200_OK
        )
    
class TestGroupViewSet(viewsets.ModelViewSet):
    queryset = TestGroup.objects.all()
    serializer_class = TestGroupSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        data = request.data.copy()
        if not user.is_staff and instance.created_by.id != user.id:
            return Response({"error": "You are not allowed to update this object."},
                        status=status.HTTP_403_FORBIDDEN)
        if 'created_by' in data:
            del data['created_by']
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        # data['created_by'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        data = request.data.copy()
        if not user.is_staff and instance.created_by.id != user.id:
            return Response({"error": "You are not allowed to update this object."},
                        status=status.HTTP_403_FORBIDDEN)
        if 'created_by' in data:
            del data['created_by']
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request,*args, **kwargs):
        data = request.data.copy()
        serializers = self.get_serializer(data=data)
        serializers.is_valid(raise_exception=True)
        serializers.save(created_by=request.user)
        return Response(serializers.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        data = request.data.copy()
        if not user.is_staff and instance.created_by.id !=user.id:
            return Response({"error":"You are not allowed to updated this objects."},
                            status=status.HTTP_403_FORBIDDEN)
        if 'created_by' in data:
            del data['created_by']
            serializers = self.get_serializer(instance, data=data, partial=True)
            serializers.is_valid(raise_exception=True)
            serializers.save()
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Package deleted successfully"},
            status=status.HTTP_200_OK
        )
    
    

    

    
    

