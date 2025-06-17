from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import PhysicianViewSet, AppointmentViewSet, DepartmentViewSet, PatientViewSet, NurseViewSet, StatisticsViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'statistics', StatisticsViewSet, basename='statistics')
router.register(r'physicians', PhysicianViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'nurses', NurseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    # Swagger UI endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),    
]

