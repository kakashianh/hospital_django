# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import Physician, Appointment, Department, AffiliatedWith, Procedures, Patient, Prescribes, OnCall, Room, Nurse, TrainedIn, Stay, Undergoes, Medication, Block
from djoser.serializers import UserSerializer, UserCreateSerializer as BaseUserSerializer

class PhysicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Physician
        fields = ["employee_id", "name", "position", "ssn"]

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = '__all__'

class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'username', 'password']

class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'email', 'username', 'password']
