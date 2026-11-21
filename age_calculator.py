"""
Core age calculation logic and command-line interface.
Handles calendar arithmetic, leap years, varying month lengths, and input validation.
"""

import calendar
import os
from datetime import date, datetime
from typing import Optional

# Enable ANSI escape codes on Windows terminal
if os.name == "nt":
    os.system("")

# ANSI terminal colors
C_PURPLE = "\033[95m"
C_SKY_BLUE = "\033[96m"
C_YELLOW = "\033[93m"
C_ORANGE = "\033[38;5;208m"
C_RESET = "\033[0m"
C_BOLD = "\033[1m"


def is_leap_year(year: int) -> bool:
    """Check if a given year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def get_month_days(year: int, month: int) -> int:
    """Return the number of days in a given month and year."""
    return calendar.monthrange(year, month)[1]


def validate_date(year: int, month: int, day: int) -> date:
    """Validate calendar numbers and return a date object."""
    if year < 1900 or year > 2100:
        raise ValueError(f"Year {year} is out of realistic range (1900 - 2100).")

    if not (1 <= month <= 12):
        raise ValueError(f"Month must be between 1 and 12, got {month}.")

    max_days = get_month_days(year, month)
    if day < 1 or day > max_days:
        month_name = calendar.month_name[month]
        if month == 2 and day == 29:
            raise ValueError(f"{year} is not a leap year, so February has only 28 days.")
        raise ValueError(f"{month_name} {year} has only {max_days} days. Day {day} is invalid.")

    return date(year, month, day)


def parse_date(date_str: str) -> date:
    """Parse date strings formatted as YYYY-MM-DD or DD/MM/YYYY."""
    cleaned = date_str.strip()
    if not cleaned:
        raise ValueError("Date input cannot be empty.")

    for sep in ["-", "/", "."]:
        if sep in cleaned:
            parts = cleaned.split(sep)
            if len(parts) == 3 and all(p.isdigit() for p in parts):
                p1, p2, p3 = int(parts[0]), int(parts[1]), int(parts[2])
                # YYYY-MM-DD
                if p1 >= 1000:
                    return validate_date(p1, p2, p3)
                # DD-MM-YYYY or MM-DD-YYYY
                elif p3 >= 1000:
                    if p1 > 12:
                        return validate_date(p3, p2, p1)
                    elif p2 > 12:
                        return validate_date(p3, p1, p2)
                    return validate_date(p3, p2, p1)

    raise ValueError(f"Invalid date format '{cleaned}'. Please use YYYY-MM-DD or DD/MM/YYYY.")


def add_months(source_date: date, months: int) -> date:
    """
    Advance a date by N calendar months.
    Clamps day if target month has fewer days (e.g. Jan 31 + 1 month -> Feb 28 or 29).
    """
    total_months = source_date.month - 1 + months
    year = source_date.year + total_months // 12
    month = total_months % 12 + 1
    day = min(source_date.day, get_month_days(year, month))
    return date(year, month, day)


def calculate_age(dob: date, target_date: Optional[date] = None) -> dict:
    """
    Calculate exact age in years, months, and days.
    Uses calendar month stepping to accurately handle leap years and month boundaries.
    """
    if target_date is None:
        target_date = date.today()

    if dob > target_date:
        raise ValueError(f"Birth date ({dob}) cannot be in the future (today is {target_date}).")

    total_months = (target_date.year - dob.year) * 12 + (target_date.month - dob.month)
    if target_date < add_months(dob, total_months):
        total_months -= 1

    years = total_months // 12
    months = total_months % 12
    anchor_date = add_months(dob, total_months)
    days = (target_date - anchor_date).days

    total_days = (target_date - dob).days

    # Next birthday resolution (handles leap day birthdays in non-leap years)
    def get_bday(year: int) -> date:
        if dob.month == 2 and dob.day == 29 and not is_leap_year(year):
            return date(year, 2, 28)
        return date(year, dob.month, dob.day)

    bday_this_year = get_bday(target_date.year)
    if bday_this_year >= target_date:
        next_bday = bday_this_year
    else:
        next_bday = get_bday(target_date.year + 1)

    days_to_bday = (next_bday - target_date).days

    return {
        "dob": dob,
        "target_date": target_date,
        "years": years,
        "months": months,
        "days": days,
        "total_days": total_days,
        "total_weeks": round(total_days / 7, 1),
        "total_hours": total_days * 24,
        "day_of_week": dob.strftime("%A"),
        "is_leap_year_born": is_leap_year(dob.year),
        "next_birthday": next_bday,
        "days_until_next_birthday": days_to_bday,
        "is_birthday_today": (days_to_bday == 0),
    }


def run_cli() -> None:
    """Run an interactive CLI session."""
    print(f"\n{C_PURPLE}{C_BOLD}{'=' * 50}")
    print("             AGE CALCULATOR (CLI)")
    print(f"{'=' * 50}{C_RESET}")

    while True:
        user_input = input(f"\n{C_BOLD}Enter Date of Birth (YYYY-MM-DD or DD/MM/YYYY):{C_RESET} ").strip()
        if not user_input:
            print(f"{C_ORANGE}Please enter a valid date.{C_RESET}")
            continue

        try:
            dob = parse_date(user_input)
            res = calculate_age(dob)

            print("\n" + f"{C_SKY_BLUE}{'-' * 46}{C_RESET}")
            age_str = (
                f"{C_PURPLE}{C_BOLD}{res['years']} Years{C_RESET}, "
                f"{C_SKY_BLUE}{C_BOLD}{res['months']} Months{C_RESET}, "
                f"{C_YELLOW}{C_BOLD}{res['days']} Days{C_RESET}"
            )
            print(f"  {C_BOLD}Exact Age        :{C_RESET} {age_str}")
            print(f"  {C_BOLD}Total Days Lived :{C_RESET} {C_SKY_BLUE}{res['total_days']:,} days{C_RESET} ({res['total_weeks']:,} weeks)")
            print(f"  {C_BOLD}Born on a        :{C_RESET} {C_PURPLE}{res['day_of_week']}{C_RESET}")
            print(f"  {C_BOLD}Leap Year Born   :{C_RESET} {'Yes' if res['is_leap_year_born'] else 'No'}")

            if res["is_birthday_today"]:
                print(f"\n  {C_YELLOW}{C_BOLD}🎂 Happy Birthday! Today is your special day! 🎉{C_RESET}")
            else:
                next_date_str = res["next_birthday"].strftime("%d %B %Y")
                print(f"  {C_BOLD}Next Birthday    :{C_RESET} {C_ORANGE}{next_date_str} ({res['days_until_next_birthday']} days left){C_RESET}")
            print(f"{C_SKY_BLUE}{'-' * 46}{C_RESET}")

        except ValueError as err:
            print(f"{C_ORANGE}Error: {err}{C_RESET}")

        again = input(f"\n{C_BOLD}Calculate another age? (y/n):{C_RESET} ").strip().lower()
        if again != "y":
            print(f"{C_PURPLE}Goodbye!{C_RESET}\n")
            break


if __name__ == "__main__":
    run_cli()
