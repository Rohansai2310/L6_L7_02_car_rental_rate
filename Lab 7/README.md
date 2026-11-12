# L6_L7_02 — Car Rental Rate

Lab 7: Fuzz Testing with Hypothesis

## About

A set of property-based fuzz tests targeting vehicle license formatting, trip mileage list processing, and rental record parsing routines to uncover edge-case parsing exceptions.

## Files

| File | Description |
|------|-------------|
| `processor.py` | The module under test (buggy starter code) |
| `test_processor.py` | Completed Hypothesis fuzz tests |
| `Lab_7_FuzzTesting_Report.pdf` | Submission report with terminal-output evidence |

## Run the lab

```bash
python -m venv .venv
.venv/bin/pip install hypothesis pytest
.venv/bin/python processor.py
.venv/bin/python -m pytest test_processor.py -q
```

The processor accepts untrusted input safely: missing license plates produce an
empty string, invalid mileage fields are skipped, and invalid rental records
return a clear validation message.

Refer to the lab handout for instructions.
