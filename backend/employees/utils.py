"""
Labour hours calculation utilities for the Aperture Labs time tracking app.

Time periods:
    Period 1 (Morning):    05:00 - 12:00
    Period 2 (Afternoon):  12:00 - 18:00
    Period 3 (Evening):    18:00 - 23:00
    Period 4 (Late Night): 23:00 - 05:00 (next day)
"""

from datetime import timedelta

# Period boundaries as (start_hour, end_hour) tuples.
# Period 4 wraps midnight, so it is split into two segments.
PERIODS = [
    ("period1", 5, 12),   # Morning
    ("period2", 12, 18),  # Afternoon
    ("period3", 18, 23),  # Evening
    # Period 4 is handled as two segments: 23:00-24:00 and 00:00-05:00
]


def calculate_labour_hours(clock_in, clock_out):
    """
    Calculate the number of hours a shift contributes to each time period.

    Args:
        clock_in: datetime of shift start
        clock_out: datetime of shift end

    Returns:
        dict with keys period1, period2, period3, period4 and float values
        rounded to 1 decimal place.
    """
    totals = {
        "period1": 0.0,
        "period2": 0.0,
        "period3": 0.0,
        "period4": 0.0,
    }

    if clock_out <= clock_in:
        return totals

    current = clock_in

    while current < clock_out:
        # Determine the date of the current position
        day_start = current.replace(hour=0, minute=0, second=0, microsecond=0)

        # Build ordered boundaries for this calendar day
        boundaries = [
            (
                "period4",
                day_start +
                timedelta(hours=0),
                day_start +
                timedelta(hours=5)
            ),
            ("period1", day_start + timedelta(hours=5),
             day_start + timedelta(hours=12)),
            ("period2", day_start + timedelta(hours=12),
             day_start + timedelta(hours=18)),
            ("period3", day_start + timedelta(hours=18),
             day_start + timedelta(hours=23)),
            ("period4", day_start + timedelta(hours=23),
             day_start + timedelta(hours=24)),
        ]

        for period_name, period_start, period_end in boundaries:
            if current >= period_end:
                continue
            if current < period_start:
                # current is before this period; periods are ordered so break
                # is wrong here -- we need to jump to this period's start
                # Actually, current should always be >= some period start.
                # If current < period_start, it means the shift starts in a
                # gap, which shouldn't happen since periods cover the full day.
                pass

            # Overlap: [current, clock_out) ∩ [period_start, period_end)
            overlap_start = max(current, period_start)
            overlap_end = min(clock_out, period_end)

            if overlap_start < overlap_end:
                hours = (overlap_end - overlap_start).total_seconds() / 3600.0
                totals[period_name] += hours

        # Move to the next day
        next_day = day_start + timedelta(days=1)
        current = next_day

    # Round to 1 decimal place
    return {k: round(v, 1) for k, v in totals.items()}


def calculate_labour_hours_for_employee(clocks):
    """
    Calculate labour hours breakdown by date for a list of clock entries.

    Args:
        clocks: queryset or list of Clock model instances

    Returns:
        list of dicts, each with date, period1-4, and total_hours
    """
    results = []
    for clock in clocks:
        hours = calculate_labour_hours(
            clock.clock_in_datetime,
            clock.clock_out_datetime
        )
        total = round(sum(hours.values()), 1)
        results.append({
            "date": clock.clock_in_datetime.strftime("%Y-%m-%d"),
            "clock_in": clock.clock_in_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "clock_out":
                clock.clock_out_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "period1": hours["period1"],
            "period2": hours["period2"],
            "period3": hours["period3"],
            "period4": hours["period4"],
            "total_hours": total,
        })
    return results
