from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters
filter_backends = [filters.SearchFilter]
from datetime import date
from .models import Physician, Appointment, Department, Patient, Nurse
from .serializers import PhysicianSerializer, AppointmentSerializer, DepartmentSerializer, PatientSerializer, NurseSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated

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


    def put(self, request, employee_id, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(employee_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = TodoSerializer(instance = todo_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, employee_id, *args, **kwargs):
        '''
        Deletes the todo item with given physician_id if exists
        '''
        todo_instance = self.get_object(employee_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

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
