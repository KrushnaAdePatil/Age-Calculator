"""
Main entry point for Age Calculator.
Supports Desktop GUI (default), interactive CLI (--cli), or command-line execution (--dob).
"""

import sys
from datetime import date

from age_calculator import (
    C_BOLD,
    C_ORANGE,
    C_PURPLE,
    C_RESET,
    C_SKY_BLUE,
    C_YELLOW,
    calculate_age,
    parse_date,
    run_cli,
)
from gui import launch_gui


def run_tests() -> None:
    """Run verification tests covering leap years, month boundaries, and edge cases."""
    print("Running verification tests...")
    test_cases = [
        (date(2000, 1, 15), date(2024, 3, 20), 24, 2, 5),
        (date(2000, 1, 25), date(2024, 3, 10), 24, 1, 14),
        (date(2024, 2, 29), date(2025, 2, 28), 1, 0, 0),
        (date(2024, 2, 29), date(2025, 3, 1), 1, 0, 1),
        (date(2024, 1, 31), date(2024, 2, 29), 0, 1, 0),
        (date(2024, 1, 31), date(2024, 3, 1), 0, 1, 1),
        (date(2020, 2, 29), date(2024, 2, 29), 4, 0, 0),
    ]

    for dob, tgt, exp_y, exp_m, exp_d in test_cases:
        res = calculate_age(dob, tgt)
        assert (res["years"], res["months"], res["days"]) == (exp_y, exp_m, exp_d), (
            f"Failed for {dob} -> {tgt}: got {(res['years'], res['months'], res['days'])}, expected {(exp_y, exp_m, exp_d)}"
        )
    print("All tests passed successfully!")


def main() -> None:
    if "--test" in sys.argv:
        run_tests()
        return

    if "--cli" in sys.argv:
        run_cli()
        return

    if "--dob" in sys.argv:
        try:
            dob_idx = sys.argv.index("--dob") + 1
            dob_str = sys.argv[dob_idx]
            dob = parse_date(dob_str)

            target = date.today()
            if "--target" in sys.argv:
                tgt_idx = sys.argv.index("--target") + 1
                target = parse_date(sys.argv[tgt_idx])

            res = calculate_age(dob, target)
            print(f"\n{C_SKY_BLUE}{'-' * 46}{C_RESET}")
            age_str = (
                f"{C_PURPLE}{C_BOLD}{res['years']} Years{C_RESET}, "
                f"{C_SKY_BLUE}{C_BOLD}{res['months']} Months{C_RESET}, "
                f"{C_YELLOW}{C_BOLD}{res['days']} Days{C_RESET}"
            )
            print(f"  {C_BOLD}Age              :{C_RESET} {age_str}")
            print(f"  {C_BOLD}Total Days Lived :{C_RESET} {C_SKY_BLUE}{res['total_days']:,} days{C_RESET} ({res['total_weeks']:,} weeks)")
            print(f"  {C_BOLD}Born on a        :{C_RESET} {C_PURPLE}{res['day_of_week']}{C_RESET}")
            if res["is_birthday_today"]:
                print(f"  {C_YELLOW}{C_BOLD}🎂 Happy Birthday! Today is your day! 🎉{C_RESET}")
            else:
                next_str = res["next_birthday"].strftime("%d %B %Y")
                print(f"  {C_BOLD}Next Birthday    :{C_RESET} {C_ORANGE}{next_str} ({res['days_until_next_birthday']} days left){C_RESET}")
            print(f"{C_SKY_BLUE}{'-' * 46}{C_RESET}\n")
        except (IndexError, ValueError) as err:
            print(f"{C_ORANGE}Error: {err}{C_RESET}")
            sys.exit(1)
        return

    launch_gui()


if __name__ == "__main__":
    main()
