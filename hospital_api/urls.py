# todo/todo_api/urls.py : API urls.py
from django.urls import path, include
from .views import (
    PhysicianListApiView,
)

urlpatterns = [
    path('api', PhysicianListApiView.as_view()),
]
