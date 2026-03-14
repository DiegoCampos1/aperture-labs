import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                ("first_name", models.CharField(max_length=100)),
                (
                    "last_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="Clock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("clock_in_datetime", models.DateTimeField()),
                ("clock_out_datetime", models.DateTimeField()),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clocks",
                        to="employees.employee",
                    ),
                ),
            ],
            options={
                "ordering": ["clock_in_datetime"],
            },
        ),
    ]
