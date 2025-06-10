from rest_framework import viewsets, permissions
from .models import Physician, Appointment
from .serializers import PhysicianSerializer, AppointmentSerializer

class PhysicianViewSet(viewsets.ModelViewSet):
    queryset = Physician.objects.all()
    serializer_class = PhysicianSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def get_queryset(self):
        physician_id = self.request.query_params.get('Physician')
        if physician_id:
            return Appointment.objects.filter(physician_id=physician_id)
        return Appointment.objects.all()