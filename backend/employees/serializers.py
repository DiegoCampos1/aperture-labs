from rest_framework import serializers

from .models import Employee


class EmployeeListSerializer(serializers.ModelSerializer):
    total_hours = serializers.FloatField(read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "total_hours"]
