"""Tests used for the Lab 6 branch-coverage submission."""

import pytest

from car_rental_rate import check_fleet_telematics, process_rental_fleet


def test_invalid_rental_list_raises_value_error():
    with pytest.raises(ValueError):
        process_rental_fleet("not a list", 10.0)


def test_negative_admin_fee_raises_value_error():
    with pytest.raises(ValueError):
        process_rental_fleet([], -1.0)


def test_unconfirmed_and_invalid_day_rentals_produce_empty_batch():
    rentals = [
        {"is_confirmed": False},
        {"is_confirmed": True, "days": 0},
    ]

    assert process_rental_fleet(rentals, 10.0) == {
        "total_revenue": 0.0,
        "status": "EMPTY_BATCH",
    }


def test_luxury_young_driver_with_standard_segment():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "luxury",
            "driver_age": 22,
            "days": 1,
            "trip_segments": [100],
        }
    ]

    assert process_rental_fleet(rentals, 10.0) == {
        "total_revenue": 200.0,
        "status": "STANDARD",
    }


def test_suv_adult_driver_with_long_segment():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "suv",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [400],
        }
    ]

    assert process_rental_fleet(rentals, 10.0) == {
        "total_revenue": 240.0,
        "status": "STANDARD",
    }


def test_economy_young_driver_long_trip_breaks_remaining_segments():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 20,
            "days": 1,
            "trip_segments": [500, 100],
        }
    ]

    assert process_rental_fleet(rentals, 10.0) == {
        "total_revenue": 320.0,
        "status": "STANDARD",
    }


def test_negative_segment_is_flagged_and_non_luxury_young_driver_fee_applies():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 22,
            "days": 1,
            "trip_segments": [-5],
        }
    ]

    assert process_rental_fleet(rentals, 10.0) == {
        "total_revenue": 70.0,
        "status": "STANDARD",
    }


def test_defaults_and_empty_segment_list_are_supported():
    assert process_rental_fleet([{"is_confirmed": True}], 0.0) == {
        "total_revenue": 40.0,
        "status": "STANDARD",
    }


def test_more_than_four_risk_flags_requires_audit():
    rentals = [{"is_confirmed": True, "days": 0} for _ in range(5)]

    assert process_rental_fleet(rentals, 10.0) == {
        "total_revenue": 0.0,
        "status": "HIGH_RISK_AUDIT",
    }


def test_telematics_no_data_safe_and_grounded_vehicle_outcomes():
    assert check_fleet_telematics([]) == "NO_DATA"
    assert check_fleet_telematics([[]]) == "SAFE"
    assert check_fleet_telematics([[101, 80, 101]]) == "SAFE"
    assert check_fleet_telematics([[101, 102]]) == "GROUND_VEHICLE"
