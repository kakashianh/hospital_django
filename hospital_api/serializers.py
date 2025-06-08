# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import Physician
class PhysicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Physician
        fields = ["employee_id", "name", "position", "ssn", "created_at", "created_by"]