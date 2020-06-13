from django.urls import path, include
from . import views


urlpatterns = [
    path('list/<int:user_id>', views.GetListView.as_view()),
    path('add', views.AddView.as_view())
]
