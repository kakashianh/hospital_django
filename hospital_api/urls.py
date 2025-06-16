from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhysicianViewSet, AppointmentViewSet, DepartmentViewSet, PatientViewSet, NurseViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'physicians', PhysicianViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'nurses', NurseViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Swagger UI endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),    
]
