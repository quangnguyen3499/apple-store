from django.urls import path, include

urlpatterns = [
    path('users/', include('platform_backend.users.urls')),
]
