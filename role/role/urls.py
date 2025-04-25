
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('userapp.urls')),
    path('api/frontdesk/', include('frontdesk.urls')),
    # path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),
]

