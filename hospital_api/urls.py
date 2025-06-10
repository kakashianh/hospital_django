# todo/todo_api/urls.py : API urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PhysicianViewSet,
)

router = DefaultRouter()
router.register(r'physicians', PhysicianViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
