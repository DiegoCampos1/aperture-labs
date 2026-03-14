from datetime import datetime

from django.test import TestCase
from rest_framework.test import APITestCase

from .models import Clock, Employee
from .utils import calculate_labour_hours


class LabourHoursCalculationTest(TestCase):
    """Tests for the labour hours calculation utility."""

    def test_morning_shift(self):
        """A shift entirely within Period 1 (Morning: 05:00-12:00)."""
        clock_in = datetime(2024, 1, 15, 6, 0, 0)
        clock_out = datetime(2024, 1, 15, 10, 0, 0)
        result = calculate_labour_hours(clock_in, clock_out)
        self.assertEqual(result["period1"], 4.0)
        self.assertEqual(result["period2"], 0.0)
        self.assertEqual(result["period3"], 0.0)
        self.assertEqual(result["period4"], 0.0)

    def test_afternoon_shift(self):
        """A shift entirely within Period 2 (Afternoon: 12:00-18:00)."""
        clock_in = datetime(2024, 1, 15, 12, 0, 0)
        clock_out = datetime(2024, 1, 15, 18, 0, 0)
        result = calculate_labour_hours(clock_in, clock_out)
        self.assertEqual(result["period1"], 0.0)
        self.assertEqual(result["period2"], 6.0)
        self.assertEqual(result["period3"], 0.0)
        self.assertEqual(result["period4"], 0.0)

    def test_evening_shift(self):
        """A shift entirely within Period 3 (Evening: 18:00-23:00)."""
        clock_in = datetime(2024, 1, 15, 18, 0, 0)
        clock_out = datetime(2024, 1, 15, 23, 0, 0)
        result = calculate_labour_hours(clock_in, clock_out)
        self.assertEqual(result["period1"], 0.0)
        self.assertEqual(result["period2"], 0.0)
        self.assertEqual(result["period3"], 5.0)
        self.assertEqual(result["period4"], 0.0)

    def test_late_night_shift(self):
        """A shift entirely within Period 4 (Late Night: 23:00-05:00)."""
        clock_in = datetime(2024, 1, 15, 23, 0, 0)
        clock_out = datetime(2024, 1, 16, 5, 0, 0)
        result = calculate_labour_hours(clock_in, clock_out)
        self.assertEqual(result["period1"], 0.0)
        self.assertEqual(result["period2"], 0.0)
        self.assertEqual(result["period3"], 0.0)
        self.assertEqual(result["period4"], 6.0)

    def test_cross_period_shift(self):
        """A shift spanning morning and afternoon."""
        clock_in = datetime(2024, 1, 15, 9, 0, 0)
        clock_out = datetime(2024, 1, 15, 14, 50, 59)
        result = calculate_labour_hours(clock_in, clock_out)
        # 9:00-12:00 = 3h morning, 12:00-14:50:59 = 2h50m59s afternoon
        self.assertEqual(result["period1"], 3.0)
        self.assertAlmostEqual(result["period2"], 2.8, places=1)

    def test_overnight_shift(self):
        """Doug Rattmann's overnight shift: 19:30 to 03:04 next day."""
        clock_in = datetime(2017, 2, 4, 19, 30, 36)
        clock_out = datetime(2017, 2, 5, 3, 4, 41)
        result = calculate_labour_hours(clock_in, clock_out)
        # 19:30:36-23:00 = period3 (evening), ~3.5h
        # 23:00-00:00 = period4 (late night), 1h
        # 00:00-03:04:41 = period4 (late night), ~3.1h
        self.assertGreater(result["period3"], 3.0)
        self.assertGreater(result["period4"], 4.0)
        total = sum(result.values())
        self.assertAlmostEqual(total, 7.6, places=1)

    def test_full_day_shift(self):
        """GLaDOS shift: nearly 48 hours spanning two full days."""
        clock_in = datetime(2012, 11, 12, 0, 0, 0)
        clock_out = datetime(2012, 11, 13, 23, 59, 59)
        result = calculate_labour_hours(clock_in, clock_out)
        total = sum(result.values())
        self.assertAlmostEqual(total, 48.0, places=0)

    def test_same_time_returns_zeros(self):
        """If clock_in equals clock_out, all periods should be zero."""
        clock_in = datetime(2024, 1, 15, 10, 0, 0)
        clock_out = datetime(2024, 1, 15, 10, 0, 0)
        result = calculate_labour_hours(clock_in, clock_out)
        self.assertEqual(result["period1"], 0.0)
        self.assertEqual(result["period2"], 0.0)
        self.assertEqual(result["period3"], 0.0)
        self.assertEqual(result["period4"], 0.0)

    def test_cave_johnson_shift(self):
        """Cave Johnson: 09:01:12 - 14:50:59."""
        clock_in = datetime(1953, 7, 20, 9, 1, 12)
        clock_out = datetime(1953, 7, 20, 14, 50, 59)
        result = calculate_labour_hours(clock_in, clock_out)
        total = sum(result.values())
        self.assertAlmostEqual(total, 5.8, places=1)


class EmployeeAPITest(APITestCase):
    """Tests for the Employee API endpoints."""

    def setUp(self):
        """Create test employees and clock entries."""
        # Clear any data from seed migration
        Clock.objects.all().delete()
        Employee.objects.all().delete()

        self.cave = Employee.objects.create(
            id=0, first_name="Cave", last_name="Johnson"
        )
        self.chell = Employee.objects.create(
            id=1, first_name="Chell", last_name="Johnson"
        )
        self.doug = Employee.objects.create(
            id=2, first_name="Doug", last_name="Rattmann"
        )
        self.glados = Employee.objects.create(
            id=3, first_name="GLaDOS", last_name=None
        )

        Clock.objects.create(
            employee=self.cave,
            clock_in_datetime="1953-07-20 09:01:12",
            clock_out_datetime="1953-07-20 14:50:59",
        )
        Clock.objects.create(
            employee=self.chell,
            clock_in_datetime="2017-02-07 10:05:12",
            clock_out_datetime="2017-02-07 14:50:59",
        )
        Clock.objects.create(
            employee=self.doug,
            clock_in_datetime="2017-02-04 19:30:36",
            clock_out_datetime="2017-02-05 03:04:41",
        )

    def test_employee_list(self):
        """GET /api/employees/ returns all employees with total_hours."""
        response = self.client.get("/api/employees/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 4)

        # Check that each employee has the expected fields
        for emp in data:
            self.assertIn("id", emp)
            self.assertIn("first_name", emp)
            self.assertIn("last_name", emp)
            self.assertIn("total_hours", emp)

    def test_employee_list_total_hours(self):
        """Verify total_hours values are calculated correctly."""
        response = self.client.get("/api/employees/")
        data = response.json()
        cave_data = next(e for e in data if e["id"] == 0)
        self.assertAlmostEqual(cave_data["total_hours"], 5.8, places=1)

    def test_search_by_last_name(self):
        """Search for employees by last name."""
        response = self.client.get("/api/employees/?search=Johnson")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        names = {e["first_name"] for e in data}
        self.assertIn("Cave", names)
        self.assertIn("Chell", names)

    def test_search_by_first_name(self):
        """Search for employees by first name."""
        response = self.client.get("/api/employees/?search=doug")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["first_name"], "Doug")

    def test_search_partial_match(self):
        """Partial match search works."""
        response = self.client.get("/api/employees/?search=john")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)

    def test_search_no_results(self):
        """Search with no matching employees returns empty list."""
        response = self.client.get("/api/employees/?search=nonexistent")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)

    def test_search_case_insensitive(self):
        """Search is case-insensitive."""
        response = self.client.get("/api/employees/?search=CAVE")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["first_name"], "Cave")

    def test_labour_detail(self):
        """GET /api/employees/{id}/labour/ returns labour breakdown."""
        response = self.client.get("/api/employees/0/labour/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], 0)
        self.assertEqual(data["first_name"], "Cave")
        self.assertIn("labour", data)
        self.assertEqual(len(data["labour"]), 1)

        labour = data["labour"][0]
        self.assertIn("period1", labour)
        self.assertIn("period2", labour)
        self.assertIn("period3", labour)
        self.assertIn("period4", labour)
        self.assertIn("total_hours", labour)

    def test_labour_detail_not_found(self):
        """GET /api/employees/{id}/labour/ returns 404 for unknown employee."""
        response = self.client.get("/api/employees/999/labour/")
        self.assertEqual(response.status_code, 404)

    def test_employee_with_no_clocks(self):
        """Employee with zero clock entries has total_hours of 0."""
        response = self.client.get("/api/employees/")
        data = response.json()
        glados_data = next(e for e in data if e["id"] == 3)
        self.assertEqual(glados_data["total_hours"], 0.0)
