from django.db import models
from userapp.models import CustomUser

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ],
        blank=True,
        null=True
    )
    age = models.PositiveIntegerField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    ipList = models.TextField(blank=True, null=True)  # Assuming this is a list of IPs as text
    commission = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bdo = models.CharField(max_length=255, blank=True, null=True)
    altPhone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    workArea = models.CharField(max_length=255, blank=True, null=True)
    degree = models.CharField(max_length=255, blank=True, null=True)
    regNumber = models.CharField(max_length=255, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Unnamed"


class TestGroup(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    # created_by = models.OneToOneField(CustomUser, on_delete=models.CASCADE , editable=False)
    status = models.BooleanField(choices=((True, 'Active'), (False, 'Inactive')), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Test(models.Model):
    group = models.ForeignKey(TestGroup, on_delete=models.CASCADE)
    # created_by = models.OneToOneField(CustomUser, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    sample_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name  


    


