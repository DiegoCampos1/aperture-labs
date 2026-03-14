import json
import os

from django.db import migrations


def seed_data(apps, schema_editor):
    """Load employee and clock data from the fixtures JSON file."""
    Employee = apps.get_model("employees", "Employee")
    Clock = apps.get_model("employees", "Clock")

    fixture_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "fixtures",
        "apertureLabsClocks.json",
    )

    with open(fixture_path, "r") as f:
        data = json.load(f)

    for emp_data in data["employees"]:
        Employee.objects.create(
            id=emp_data["id"],
            first_name=emp_data["first_name"],
            last_name=emp_data.get("last_name"),
        )

    for clock_data in data["clocks"]:
        Clock.objects.create(
            employee_id=clock_data["employee_id"],
            clock_in_datetime=clock_data["clock_in_datetime"],
            clock_out_datetime=clock_data["clock_out_datetime"],
        )


def reverse_seed_data(apps, schema_editor):
    """Remove seeded data."""
    Employee = apps.get_model("employees", "Employee")
    Clock = apps.get_model("employees", "Clock")
    Clock.objects.all().delete()
    Employee.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_seed_data),
    ]
