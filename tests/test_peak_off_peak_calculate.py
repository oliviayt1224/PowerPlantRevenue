from src import functions
import pytest

@pytest.mark.parametrize("month, peak_hours, off_peak_hours, days_in_month", [
    ("2025/2", 280, 392, 28),

])

def test_peak_off_peak_calculation(month, peak_hours, off_peak_hours, days_in_month):
    sim = functions.Simulation()
    sim.targeted_month = month
    assert list(sim.calculate_peak_and_off_peak_hours()) == [peak_hours, off_peak_hours, days_in_month]

