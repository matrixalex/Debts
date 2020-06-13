from django.urls import path, include


urlpatterns = [
    path('', include('apps.main_app.urls')),
    path('auth/', include('apps.users.urls')),
    path('api/', include('apps.api.urls')),
]
