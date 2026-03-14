from django.db import models


class Employee(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name


class Clock(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="clocks",
    )
    clock_in_datetime = models.DateTimeField()
    clock_out_datetime = models.DateTimeField()

    class Meta:
        ordering = ["clock_in_datetime"]

    def __str__(self):
        return (
            f"{self.employee} | "
            f"{self.clock_in_datetime} - {self.clock_out_datetime}"
        )
