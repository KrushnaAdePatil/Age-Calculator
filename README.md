# Exact Age Calculator

A Python project that calculates a person's exact age in years, months, and days from their date of birth. It accurately accounts for leap years, varying month lengths (28, 29, 30, and 31 days), and validates user inputs against future or impossible dates.

The project includes both a modern desktop graphical interface (Tkinter) and a command-line interface (CLI).

---

## The Problem with Simple Division

A common mistake when calculating age in code is dividing total days by 365 or 365.25:

```python
# Inaccurate approach
age_years = (today - dob).days / 365.25
```

This approach leads to errors because:
1. Calendar months vary in length (February has 28 or 29 days, while other months have 30 or 31 days).
2. Leap years add an extra day every 4 years, which affects birthdays unevenly depending on which months have passed.
3. Someone born on January 31 reaching February 28 has completed one full calendar month, but simple day counting cannot represent this accurately without month-level alignment.

This project solves these issues with a calendar-aware month-stepping algorithm.

---

## Features

- **Exact Calendar Calculation**: Calculates exact elapsed years, months, and days.
- **Leap Year Support**: Correctly handles leap years and edge cases for leap-day birthdays (February 29).
- **Month Length Clamping**: Correctly transitions between months of different lengths (e.g., January 31 to late February).
- **Strict Input Validation**: Rejects future dates, non-existent calendar dates (such as February 30 or April 31), and invalid leap-day entries (such as February 29 on non-leap years).
- **Desktop Graphical Interface (GUI)**:
  - Clean card-based design built with standard Tkinter.
  - Separate Day, Month, and Year selectors to prevent typing mistakes.
  - Segmented toggle to switch between calculating age as of today or a custom comparison date.
  - Animated number count-up reveal on calculation.
- **Interactive CLI**: Fast terminal interface with colored highlights and argument flags.
- **Lifespan Analytics**: Computes total days lived, total weeks, total hours, day of the week of birth, and a countdown to the next birthday.
- **Zero Dependencies**: Built entirely with Python's built-in standard library (`datetime`, `calendar`, `tkinter`, `os`, `sys`). No external packages needed.

---

## Project Structure

```text
Age Calculator/
│
├── age_calculator.py    # Core math engine, calendar validation, and CLI
├── gui.py               # Tkinter desktop application
├── main.py              # Main launcher (runs GUI, CLI, or tests)
└── README.md            # Documentation
```

---

## How the Algorithm Works

The calculation logic in `age_calculator.py` follows these steps:

1. **Validation**: Check that the date numbers are within normal ranges (years 1900–2100, months 1–12, and valid days for that month/year). Ensure the birth date is not after the target date.
2. **Month Stepping (`add_months`)**: Determine the total elapsed months:
   ```text
   total_months = (target.year - dob.year) * 12 + (target.month - dob.month)
   ```
   If stepping forward by `total_months` overshoots the target date, decrement `total_months` by 1.
3. **Day Clamping**: When advancing months, if the target month has fewer days than the birth day (e.g. Jan 31 advancing to February), the day is clamped to the maximum valid day of that month (`calendar.monthrange`).
4. **Remaining Days**:
   ```text
   years = total_months // 12
   months = total_months % 12
   days = (target_date - anchor_date).days
   ```
5. **Next Birthday Resolution**: Determines when the next birthday occurs. If born on February 29, it sets the birthday to February 28 during non-leap years.

---

## How to Run

### 1. Run the Desktop GUI
To launch the graphical desktop interface:

```bash
python main.py
```
*(or run `python gui.py`)*

### 2. Run the Interactive Terminal CLI
To use the interactive terminal interface:

```bash
python main.py --cli
```
*(or run `python age_calculator.py`)*

### 3. Run a Quick Calculation with Arguments
Calculate age directly without opening the interactive menu:

```bash
# Calculate age up to today
python main.py --dob 2002-05-15

# Calculate age relative to a specific target date
python main.py --dob 2000-01-15 --target 2026-11-20
```

### 4. Run the Verification Tests
To run the automated verification tests covering leap years, month transitions, and edge cases:

```bash
python main.py --test
```

---

## Edge Cases Verified

The test suite validates:
- **February 29 on Leap Years**: Born on 2020-02-29 $\to$ age on 2024-02-29 is exactly 4 years, 0 months, 0 days.
- **February 29 on Non-Leap Years**: Born on 2024-02-29 $\to$ age on 2025-02-28 is 1 year, 0 months, 0 days; on 2025-03-01 is 1 year, 0 months, 1 day.
- **Month Length Boundaries**: Born on 2024-01-31 $\to$ age on 2024-02-29 is 0 years, 1 month, 0 days; on 2024-03-01 is 0 years, 1 month, 1 day.
- **Same-Day Calculation**: Age on the day of birth is 0 years, 0 months, 0 days.
- **Invalid Date Rejection**: Flags dates like `2024-02-30`, `2023-02-29`, or `2024-04-31` with informative error messages.
