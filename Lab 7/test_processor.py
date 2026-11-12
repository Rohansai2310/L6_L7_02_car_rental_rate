from hypothesis import given, strategies as st
from processor import sanitize_license_plate, parse_trip_mileage, format_rental_invoice

@given(st.one_of(st.text(), st.none()))
def test_sanitize_license_plate_no_crash(s):
    """Any text-like license plate input should be handled safely."""
    try:
        result = sanitize_license_plate(s)
        assert isinstance(result, str)
    except Exception as exc:
        assert False, f"sanitize_license_plate crashed for {s!r}: {exc}"

@given(st.one_of(st.text(), st.none()))
def test_parse_trip_mileage_safe(s):
    """Malformed CSV input must not make the mileage parser raise."""
    try:
        result = parse_trip_mileage(s)
        assert isinstance(result, list)
        assert all(isinstance(mileage, float) for mileage in result)
    except Exception as exc:
        assert False, f"parse_trip_mileage crashed for {s!r}: {exc}"

@given(st.one_of(st.text(), st.none()))
def test_format_rental_invoice_safe(s):
    """Incomplete or invalid rental records must produce a safe response."""
    try:
        result = format_rental_invoice(s)
        assert isinstance(result, str)
    except Exception as exc:
        assert False, f"format_rental_invoice crashed for {s!r}: {exc}"
