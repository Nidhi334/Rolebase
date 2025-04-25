from django.db import models
from userapp.models import CustomUser

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
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
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    reg = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)
    joining_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name  

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


    


