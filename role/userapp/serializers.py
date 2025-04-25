from rest_framework import serializers
from userapp.models import Tenant, CustomUser, Role, Permission, Group

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'name', 'created_at']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name']

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'tenant_id', 'permissions']

class GroupSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'tenant_id', 'roles']

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'groups', 'tenant_id']
        read_only_fields = ['tenant_id']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tenant_id = serializers.UUIDField()
    role_id = serializers.IntegerField()
    group_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'tenant_id', 'role_id', 'group_ids']
    
    # def validate(self, data):
    #     if not Tenant.objects.filter(id=data['tenant_id']).exists():
    #         raise serializers.ValidationError("Invalid tenant_id")
    #     if not Role.objects.filter(id=data['role_id'], tenant_id=data['tenant_id']).exists():
    #         raise serializers.ValidationError("Invalid role_id for this tenant")
    #     return data
    
    def create(self, validated_data):
        group_ids = validated_data.pop('group_ids', [])
        role_id = validated_data.pop('role_id')
        tenant_id = validated_data.pop('tenant_id')
        
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            tenant_id=Tenant.objects.get(id=tenant_id),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        user.role = Role.objects.get(id=role_id)
        user.save()
        
        if group_ids:
            groups = Group.objects.filter(id__in=group_ids, tenant_id=tenant_id)
            user.user_groups.set(groups)
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'name', 'created_at']