from rest_framework import serializers
from .models import *
from userapp.models import *

class DoctorSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(), default=serializers.CurrentUserDefault())
    class Meta:
        model = Doctor
        fields = '__all__'

class TestGroupSerializer(serializers.ModelSerializer):
    # created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(), default=serializers.CurrentUserDefault())
    class Meta:
        model = TestGroup
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    # created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Test
        fields = '__all__'



