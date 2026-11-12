from math import isfinite


INVALID_RECORD_MESSAGE = (
    "Invalid rental record. Expected format: Driver:Days:Category "
    "with a positive whole number of days."
)


def sanitize_license_plate(plate):
    """Return an uppercase plate without supported formatting delimiters.

    Missing or non-text input is treated as an empty plate so callers that
    accept untrusted form data do not encounter an AttributeError.
    """
    if not isinstance(plate, str):
        return ""

    plate = plate.strip()
    for ch in ['-', ' ', '_', '#']:
        plate = plate.replace(ch, '')
    return plate.upper()


def parse_trip_mileage(mileage_csv):
    """Parse valid, finite mileage values from a comma-separated string.

    Blank fields and invalid numeric tokens are ignored.  This lets a single
    malformed value in user input fail safely rather than stopping processing
    of otherwise valid mileage entries.
    """
    if not isinstance(mileage_csv, str):
        return []

    mileages = []
    for part in mileage_csv.split(','):
        token = part.strip()
        if not token:
            continue
        try:
            mileage = float(token)
        except (TypeError, ValueError):
            continue
        if isfinite(mileage):
            mileages.append(mileage)
    return mileages


def format_rental_invoice(record):
    """Create an invoice for a ``Driver:Days:Category`` rental record.

    Invalid or incomplete input returns a user-facing validation message
    instead of leaking parsing exceptions to the caller.
    """
    if not isinstance(record, str):
        return INVALID_RECORD_MESSAGE

    parts = record.split(':')
    if len(parts) != 3:
        return INVALID_RECORD_MESSAGE

    driver = parts[0].strip()
    category = parts[2].strip()
    if not driver or not category:
        return INVALID_RECORD_MESSAGE

    try:
        days = int(parts[1].strip())
    except (TypeError, ValueError):
        return INVALID_RECORD_MESSAGE
    if days <= 0:
        return INVALID_RECORD_MESSAGE

    daily_rate = 50.0 if category.lower() == "suv" else 30.0
    total = days * daily_rate
    return f"Driver {driver} booked {category} for {days} days: Total ${total:.2f}"

def main():
    print("==== Running sanitize_license_plate ====")
    raw_plate = input("Enter license plate with delimiters (-, _, #): ")
    clean_plate = sanitize_license_plate(raw_plate)
    print("Sanitized Plate:", clean_plate)

    print("\n==== Running parse_trip_mileage ====")
    csv_input = input("Enter CSV of mileages (e.g. 100.5, 45.2, 80.0): ")
    mileage_list = parse_trip_mileage(csv_input)
    print("Parsed Mileage List:", mileage_list)

    print("\n==== Running format_rental_invoice ====")
    record_input = input("Enter rental record (Driver:Days:Category): ")
    invoice = format_rental_invoice(record_input)
    print("Rental Invoice:", invoice)

if __name__ == "__main__":
    main()
