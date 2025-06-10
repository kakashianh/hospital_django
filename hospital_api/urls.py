from rest_framework.routers import DefaultRouter
from .views import PhysicianViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r'physicians', PhysicianViewSet)
router.register(r'appointments', AppointmentViewSet)


urlpatterns = router.urls