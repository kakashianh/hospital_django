from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters
filter_backends = [filters.SearchFilter]
from datetime import date
from .models import Physician, Appointment, Department, Patient, Nurse
from .serializers import PhysicianSerializer, AppointmentSerializer, DepartmentSerializer, PatientSerializer, NurseSerializer

class StatisticsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        today = date.today()
        patient_count = Patient.objects.count()
        physician_count = Physician.objects.count()
        nurse_count = Nurse.objects.count()
        department_count = Department.objects.count()
        appointment_today = Appointment.objects.filter(start_time__date=today).count()

        data = {
            'total_patients': patient_count,
            'total_physicians': physician_count,
            'total_nurses': nurse_count,
            'total_departments': department_count,
            'appointments_today': appointment_today
        }
        return Response(data)

class PhysicianViewSet(viewsets.ModelViewSet):
    queryset = Physician.objects.all()
    serializer_class = PhysicianSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        physician_id = self.request.query_params.get('physician')
        patient_id = self.request.query_params.get('patient')
        if physician_id and patient_id:
            return Appointment.objects.filter(physician_id=physician_id, patient_id=patient_id)
        if physician_id:
            return Appointment.objects.filter(physician_id=physician_id)
        if patient_id:
            return Appointment.objects.filter(patient_id=patient_id)

        return Appointment.objects.all()

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]




class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['phone', 'pcp']
    search_fields = ['name']

class NurseViewSet(viewsets.ModelViewSet):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
