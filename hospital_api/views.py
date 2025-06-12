from rest_framework import viewsets, permissions
from .models import Physician, Appointment, Department, Patient, Nurse
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PhysicianSerializer, AppointmentSerializer, DepartmentSerializer, PatientSerializer, NurseSerializer

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
        physician_id = self.request.query_params.get('physician')
        patient_id = self.request.query_params.get('patient')
        if physician_id:
            return Appointment.objects.filter(physician_id=physician_id)
        if patient_id:
            return Appointment.objects.filter(patient_id=patient_id)
        if physician_id and patient_id:
            return Appointment.objects.filter(physician_id=physician_id, patient_id=patient_id)
        return Appointment.objects.all()

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class NurseViewSet(viewsets.ModelViewSet):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
