from django.urls import path
from .views import RegisterView, LoginView, UserProfileView,TenantView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('tenant/', TenantView.as_view(), name='tenant'),
    path('role/', TenantView.as_view(), name='role'),
    path('permission/', TenantView.as_view(), name='permission'),
]