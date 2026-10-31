"""Tests used for the Lab 6 line/code-coverage submission."""

import pytest

from car_rental_rate import check_fleet_telematics, process_rental_fleet


def test_invalid_arguments_raise_value_error():
    with pytest.raises(ValueError):
        process_rental_fleet("not a list", 10.0)


def test_rental_paths_and_statuses():
    rentals = [
        {"is_confirmed": False},
        {"is_confirmed": True, "days": 0},
        {
            "is_confirmed": True,
            "vehicle_type": "luxury",
            "driver_age": 22,
            "days": 1,
            "trip_segments": [100],
        },
        {
            "is_confirmed": True,
            "vehicle_type": "suv",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [400],
        },
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 20,
            "days": 1,
            "trip_segments": [-5, 500, 100],
        },
    ]

    result = process_rental_fleet(rentals, 10.0)

    assert result == {"total_revenue": 760.0, "status": "STANDARD"}


def test_empty_batch_status():
    assert process_rental_fleet([], 10.0) == {
        "total_revenue": 0.0,
        "status": "EMPTY_BATCH",
    }


def test_high_risk_audit_status():
    rentals = [{"is_confirmed": True, "days": 0} for _ in range(5)]

    assert process_rental_fleet(rentals, 10.0) == {
        "total_revenue": 0.0,
        "status": "HIGH_RISK_AUDIT",
    }


def test_telematics_results():
    assert check_fleet_telematics([]) == "NO_DATA"
    assert check_fleet_telematics([[101, 80, 101]]) == "SAFE"
    assert check_fleet_telematics([[101, 102]]) == "GROUND_VEHICLE"
