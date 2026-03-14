from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import Employee
from .serializers import EmployeeListSerializer
from .utils import calculate_labour_hours, calculate_labour_hours_for_employee


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing employees and retrieving their labour details.
    """
    serializer_class = EmployeeListSerializer

    def get_queryset(self):
        queryset = Employee.objects.all()

        # Apply search filter
        search = self.request.query_params.get("search", None)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
            )

        # Annotate each employee with total_hours calculated from their clocks
        employees = list(queryset)
        for employee in employees:
            total = 0.0
            for clock in employee.clocks.all():
                hours = calculate_labour_hours(
                    clock.clock_in_datetime, clock.clock_out_datetime
                )
                total += sum(hours.values())
            employee.total_hours = round(total, 1)

        return employees

    def list(self, request, *args, **kwargs):
        employees = self.get_queryset()
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="labour")
    def labour(self, request, pk=None):
        """Return detailed labour breakdown by shift for a single employee."""
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response(
                {"detail": "Employee not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        clocks = employee.clocks.all().order_by("clock_in_datetime")
        labour_data = calculate_labour_hours_for_employee(clocks)

        return Response({
            "id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "labour": labour_data,
        })
