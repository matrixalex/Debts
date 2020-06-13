from django.urls import path, include

urlpatterns = [
    path('debts/', include('apps.api.debts.urls')),
]
