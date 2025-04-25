import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, tenant_id, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, tenant_id=tenant_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, None, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

    def __str__(self):
        return self.email

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('role', 'permission')

class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    tenant_id = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    users = models.ManyToManyField(CustomUser, related_name='user_groups')
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return self.name