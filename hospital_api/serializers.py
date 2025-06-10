# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import Physician, Appointment
class PhysicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Physician
        fields = ["employee_id", "name", "position", "ssn"]

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'