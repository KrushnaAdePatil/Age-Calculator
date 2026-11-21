"""
Age Calculator Desktop Application (Tkinter).
Builds a clean desktop UI with segmented date controls and an animated counter reveal.
"""

import calendar
from datetime import date
import tkinter as tk
from tkinter import ttk

from age_calculator import calculate_age, validate_date


class AgeCalculatorGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Exact Age Calculator")
        self.root.geometry("540x720")
        self.root.resizable(False, False)
        self.root.configure(bg="#F8FAFC")

        self.animation_job = None
        self._configure_styles()
        self._center_window(540, 720)
        self._setup_ui()

    def _center_window(self, width: int, height: int) -> None:
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _configure_styles(self) -> None:
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure(
            "Modern.TCombobox",
            fieldbackground="#FFFFFF",
            background="#F8FAFC",
            foreground="#0F172A",
            arrowcolor="#4F46E5",
            bordercolor="#CBD5E1",
            lightcolor="#FFFFFF",
            darkcolor="#FFFFFF",
            padding=(6, 5),
            relief="flat",
        )
        self.style.map(
            "Modern.TCombobox",
            fieldbackground=[("readonly", "#FFFFFF"), ("disabled", "#F1F5F9")],
            foreground=[("readonly", "#0F172A"), ("disabled", "#94A3B8")],
            arrowcolor=[("disabled", "#CBD5E1"), ("active", "#4338CA")],
            bordercolor=[("focus", "#4F46E5"), ("active", "#6366F1"), ("disabled", "#E2E8F0")],
        )

    def _setup_ui(self) -> None:
        today = date.today()

        # Header
        header = tk.Frame(self.root, bg="#4F46E5", padx=24, pady=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🎂 Exact Age Calculator",
            font=("Segoe UI", 17, "bold"),
            bg="#4F46E5",
            fg="#FFFFFF",
        ).pack(anchor="w")

        tk.Label(
            header,
            text="High-precision calendar math • Leap years • Variable month lengths",
            font=("Segoe UI", 8),
            bg="#4F46E5",
            fg="#C7D2FE",
        ).pack(anchor="w", pady=(3, 0))

        tk.Frame(self.root, bg="#38BDF8", height=2).pack(fill="x")

        # Input Card
        card_input = tk.Frame(self.root, bg="#FFFFFF", padx=20, pady=16, highlightthickness=1, highlightbackground="#E2E8F0")
        card_input.pack(fill="x", padx=16, pady=(14, 8))

        days_list = [str(i) for i in range(1, 32)]
        months_list = [calendar.month_name[i] for i in range(1, 13)]
        years_list = [str(y) for y in range(today.year, 1919, -1)]

        # Birth date inputs
        tk.Label(card_input, text="SELECT DATE OF BIRTH", font=("Segoe UI", 8, "bold"), bg="#FFFFFF", fg="#475569").pack(anchor="w", pady=(0, 4))
        dob_grid = tk.Frame(card_input, bg="#FFFFFF")
        dob_grid.pack(fill="x", pady=(0, 14))

        col_day = tk.Frame(dob_grid, bg="#FFFFFF")
        col_day.pack(side="left", padx=(0, 12))
        tk.Label(col_day, text="Day", font=("Segoe UI", 8), bg="#FFFFFF", fg="#64748B").pack(anchor="w", pady=(0, 2))
        self.dob_day = ttk.Combobox(col_day, values=days_list, width=5, state="readonly", style="Modern.TCombobox", font=("Segoe UI", 9))
        self.dob_day.set(str(today.day))
        self.dob_day.pack()

        col_month = tk.Frame(dob_grid, bg="#FFFFFF")
        col_month.pack(side="left", padx=(0, 12))
        tk.Label(col_month, text="Month", font=("Segoe UI", 8), bg="#FFFFFF", fg="#64748B").pack(anchor="w", pady=(0, 2))
        self.dob_month = ttk.Combobox(col_month, values=months_list, width=14, state="readonly", style="Modern.TCombobox", font=("Segoe UI", 9))
        self.dob_month.set(calendar.month_name[today.month])
        self.dob_month.pack()

        col_year = tk.Frame(dob_grid, bg="#FFFFFF")
        col_year.pack(side="left")
        tk.Label(col_year, text="Year", font=("Segoe UI", 8), bg="#FFFFFF", fg="#64748B").pack(anchor="w", pady=(0, 2))
        self.dob_year = ttk.Combobox(col_year, values=years_list, width=7, style="Modern.TCombobox", font=("Segoe UI", 9))
        self.dob_year.set("2000")
        self.dob_year.pack()

        # Target date selection
        tk.Label(card_input, text="CALCULATE AGE AS OF", font=("Segoe UI", 8, "bold"), bg="#FFFFFF", fg="#475569").pack(anchor="w", pady=(0, 6))
        self.target_mode_var = tk.StringVar(value="today")

        segmented_row = tk.Frame(card_input, bg="#FFFFFF")
        segmented_row.pack(fill="x", pady=(0, 8))

        self.seg_btn_today = tk.Label(
            segmented_row,
            text=f"📅 Today's Date ({today.strftime('%d %b %Y')})",
            font=("Segoe UI", 9, "bold"),
            bg="#4F46E5",
            fg="#FFFFFF",
            padx=14,
            pady=5,
            cursor="hand2",
        )
        self.seg_btn_today.pack(side="left", padx=(0, 8))
        self.seg_btn_today.bind("<Button-1>", lambda e: self._set_target_mode("today"))

        self.seg_btn_custom = tk.Label(
            segmented_row,
            text="✏️ Custom Date",
            font=("Segoe UI", 9),
            bg="#F1F5F9",
            fg="#475569",
            padx=14,
            pady=5,
            cursor="hand2",
        )
        self.seg_btn_custom.pack(side="left")
        self.seg_btn_custom.bind("<Button-1>", lambda e: self._set_target_mode("custom"))

        # Target date dropdowns
        target_grid = tk.Frame(card_input, bg="#FFFFFF")
        target_grid.pack(fill="x", pady=(0, 14))

        target_years_list = [str(y) for y in range(today.year + 50, 1919, -1)]

        col_t_day = tk.Frame(target_grid, bg="#FFFFFF")
        col_t_day.pack(side="left", padx=(0, 12))
        self.lbl_t_day = tk.Label(col_t_day, text="Target Day", font=("Segoe UI", 8), bg="#FFFFFF", fg="#94A3B8")
        self.lbl_t_day.pack(anchor="w", pady=(0, 2))
        self.target_day = ttk.Combobox(col_t_day, values=days_list, width=5, state="disabled", style="Modern.TCombobox", font=("Segoe UI", 9))
        self.target_day.set(str(today.day))
        self.target_day.pack()

        col_t_month = tk.Frame(target_grid, bg="#FFFFFF")
        col_t_month.pack(side="left", padx=(0, 12))
        self.lbl_t_month = tk.Label(col_t_month, text="Target Month", font=("Segoe UI", 8), bg="#FFFFFF", fg="#94A3B8")
        self.lbl_t_month.pack(anchor="w", pady=(0, 2))
        self.target_month = ttk.Combobox(col_t_month, values=months_list, width=14, state="disabled", style="Modern.TCombobox", font=("Segoe UI", 9))
        self.target_month.set(calendar.month_name[today.month])
        self.target_month.pack()

        col_t_year = tk.Frame(target_grid, bg="#FFFFFF")
        col_t_year.pack(side="left")
        self.lbl_t_year = tk.Label(col_t_year, text="Target Year", font=("Segoe UI", 8), bg="#FFFFFF", fg="#94A3B8")
        self.lbl_t_year.pack(anchor="w", pady=(0, 2))
        self.target_year = ttk.Combobox(col_t_year, values=target_years_list, width=7, state="disabled", style="Modern.TCombobox", font=("Segoe UI", 9))
        self.target_year.set(str(today.year))
        self.target_year.pack()

        # Action Buttons
        btn_box = tk.Frame(card_input, bg="#FFFFFF")
        btn_box.pack(fill="x")

        self.calc_btn = tk.Button(
            btn_box,
            text="⚡ Calculate Exact Age",
            command=self.calculate_with_animation,
            bg="#F97316",
            fg="#FFFFFF",
            activebackground="#EA580C",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=7,
            cursor="hand2",
        )
        self.calc_btn.pack(side="left", padx=(0, 10))

        self.reset_btn = tk.Button(
            btn_box,
            text="Reset",
            command=self.reset,
            bg="#F1F5F9",
            fg="#475569",
            activebackground="#E2E8F0",
            font=("Segoe UI", 9),
            relief="solid",
            bd=1,
            highlightbackground="#CBD5E1",
            padx=14,
            pady=6,
            cursor="hand2",
        )
        self.reset_btn.pack(side="left")

        self.error_label = tk.Label(
            card_input,
            text="",
            bg="#FFFFFF",
            fg="#DC2626",
            font=("Segoe UI", 9, "bold"),
            wraplength=480,
            justify="left",
        )
        self.error_label.pack(anchor="w", pady=(6, 0))

        # Output Card
        self.card_output = tk.Frame(self.root, bg="#FFFFFF", padx=20, pady=16, highlightthickness=1, highlightbackground="#E2E8F0")
        self.card_output.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        tk.Label(
            self.card_output,
            text="CHRONOLOGICAL BREAKDOWN & STATS",
            font=("Segoe UI", 8, "bold"),
            bg="#FFFFFF",
            fg="#475569",
        ).pack(anchor="w", pady=(0, 8))

        # Initial Placeholder Frame
        self.placeholder_frame = tk.Frame(self.card_output, bg="#F8FAFC", padx=20, pady=40, highlightthickness=1, highlightbackground="#E2E8F0")
        self.placeholder_frame.pack(fill="both", expand=True)

        tk.Label(
            self.placeholder_frame,
            text="📊 Ready to Calculate",
            font=("Segoe UI", 13, "bold"),
            bg="#F8FAFC",
            fg="#475569",
        ).pack(pady=(0, 6))

        tk.Label(
            self.placeholder_frame,
            text="Select your Date of Birth above and click 'Calculate Exact Age'\nto open your exact age breakdown and lifespan analytics.",
            font=("Segoe UI", 9),
            bg="#F8FAFC",
            fg="#64748B",
            justify="center",
        ).pack()

        # Active Results Frame
        self.results_content_frame = tk.Frame(self.card_output, bg="#FFFFFF")

        self.summary_box = tk.Frame(self.results_content_frame, bg="#EEF2FF", padx=12, pady=8, highlightthickness=1, highlightbackground="#C7D2FE")
        self.summary_box.pack(fill="x", pady=(0, 10))

        self.lbl_age_summary = tk.Label(
            self.summary_box,
            text="",
            font=("Segoe UI", 13, "bold"),
            bg="#EEF2FF",
            fg="#3730A3",
        )
        self.lbl_age_summary.pack(anchor="w")

        # 3 Hero Cards
        hero_frame = tk.Frame(self.results_content_frame, bg="#FFFFFF")
        hero_frame.pack(fill="x", pady=(0, 10))

        card_years = tk.Frame(hero_frame, bg="#FAF5FF", padx=8, pady=10, highlightthickness=1, highlightbackground="#DDD6FE")
        card_years.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.val_years = tk.Label(card_years, text="0", font=("Segoe UI", 24, "bold"), bg="#FAF5FF", fg="#6B21A8")
        self.val_years.pack()
        tk.Label(card_years, text="YEARS", font=("Segoe UI", 8, "bold"), bg="#FAF5FF", fg="#9333EA").pack()

        card_months = tk.Frame(hero_frame, bg="#F0F9FF", padx=8, pady=10, highlightthickness=1, highlightbackground="#BAE6FD")
        card_months.pack(side="left", fill="both", expand=True, padx=5)
        self.val_months = tk.Label(card_months, text="0", font=("Segoe UI", 24, "bold"), bg="#F0F9FF", fg="#0369A1")
        self.val_months.pack()
        tk.Label(card_months, text="MONTHS", font=("Segoe UI", 8, "bold"), bg="#F0F9FF", fg="#0284C7").pack()

        card_days = tk.Frame(hero_frame, bg="#FEFCE8", padx=8, pady=10, highlightthickness=1, highlightbackground="#FEF08A")
        card_days.pack(side="left", fill="both", expand=True, padx=(5, 0))
        self.val_days = tk.Label(card_days, text="0", font=("Segoe UI", 24, "bold"), bg="#FEFCE8", fg="#854D0E")
        self.val_days.pack()
        tk.Label(card_days, text="DAYS", font=("Segoe UI", 8, "bold"), bg="#FEFCE8", fg="#CA8A04").pack()

        # Birthday Banner
        self.bday_banner = tk.Label(
            self.results_content_frame,
            text="🎂 Happy Birthday! Wishing you an incredible year ahead! 🎉",
            font=("Segoe UI", 9, "bold"),
            bg="#FEF3C7",
            fg="#92400E",
            bd=1,
            relief="solid",
            highlightbackground="#F59E0B",
            highlightthickness=1,
            pady=5,
        )

        # 2x2 Details Grid
        stats_grid = tk.Frame(self.results_content_frame, bg="#FFFFFF")
        stats_grid.pack(fill="both", expand=True)

        c1 = tk.Frame(stats_grid, bg="#F8FAFC", padx=10, pady=8, highlightthickness=1, highlightbackground="#E2E8F0")
        c1.grid(row=0, column=0, sticky="nsew", padx=(0, 4), pady=4)
        tk.Label(c1, text="⏱ TOTAL DAYS LIVED", font=("Segoe UI", 7, "bold"), bg="#F8FAFC", fg="#0284C7").pack(anchor="w")
        self.lbl_days_total = tk.Label(c1, text="0 days", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A")
        self.lbl_days_total.pack(anchor="w", pady=(2, 0))

        c2 = tk.Frame(stats_grid, bg="#F8FAFC", padx=10, pady=8, highlightthickness=1, highlightbackground="#E2E8F0")
        c2.grid(row=0, column=1, sticky="nsew", padx=(4, 0), pady=4)
        tk.Label(c2, text="🎁 NEXT BIRTHDAY", font=("Segoe UI", 7, "bold"), bg="#F8FAFC", fg="#D97706").pack(anchor="w")
        self.lbl_next_bday = tk.Label(c2, text="--", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A")
        self.lbl_next_bday.pack(anchor="w", pady=(2, 0))

        c3 = tk.Frame(stats_grid, bg="#F8FAFC", padx=10, pady=8, highlightthickness=1, highlightbackground="#E2E8F0")
        c3.grid(row=1, column=0, sticky="nsew", padx=(0, 4), pady=4)
        tk.Label(c3, text="🗓 DAY OF BIRTH", font=("Segoe UI", 7, "bold"), bg="#F8FAFC", fg="#7C3AED").pack(anchor="w")
        self.lbl_birth_info = tk.Label(c3, text="--", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A")
        self.lbl_birth_info.pack(anchor="w", pady=(2, 0))

        c4 = tk.Frame(stats_grid, bg="#F8FAFC", padx=10, pady=8, highlightthickness=1, highlightbackground="#E2E8F0")
        c4.grid(row=1, column=1, sticky="nsew", padx=(4, 0), pady=4)
        tk.Label(c4, text="⌛ TOTAL TIME", font=("Segoe UI", 7, "bold"), bg="#F8FAFC", fg="#EA580C").pack(anchor="w")
        self.lbl_total_hours = tk.Label(c4, text="0 hrs", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A")
        self.lbl_total_hours.pack(anchor="w", pady=(2, 0))

        stats_grid.columnconfigure(0, weight=1)
        stats_grid.columnconfigure(1, weight=1)

    def _set_target_mode(self, mode: str) -> None:
        self.target_mode_var.set(mode)
        is_today = (mode == "today")

        if is_today:
            self.seg_btn_today.config(bg="#4F46E5", fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
            self.seg_btn_custom.config(bg="#F1F5F9", fg="#475569", font=("Segoe UI", 9))

            today = date.today()
            self.target_day.set(str(today.day))
            self.target_month.set(calendar.month_name[today.month])
            self.target_year.set(str(today.year))

            self.target_day.config(state="disabled")
            self.target_month.config(state="disabled")
            self.target_year.config(state="disabled")

            self.lbl_t_day.config(fg="#94A3B8")
            self.lbl_t_month.config(fg="#94A3B8")
            self.lbl_t_year.config(fg="#94A3B8")
        else:
            self.seg_btn_custom.config(bg="#4F46E5", fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
            self.seg_btn_today.config(bg="#F1F5F9", fg="#475569", font=("Segoe UI", 9))

            self.target_day.config(state="readonly")
            self.target_month.config(state="readonly")
            self.target_year.config(state="normal")

            self.lbl_t_day.config(fg="#475569")
            self.lbl_t_month.config(fg="#475569")
            self.lbl_t_year.config(fg="#475569")

    def _get_dob(self) -> date:
        day = int(self.dob_day.get())
        month_name = self.dob_month.get()
        month = list(calendar.month_name).index(month_name)
        year = int(self.dob_year.get().strip())
        return validate_date(year, month, day)

    def _get_target_date(self) -> date:
        if self.target_mode_var.get() == "today":
            return date.today()
        day = int(self.target_day.get())
        month_name = self.target_month.get()
        month = list(calendar.month_name).index(month_name)
        year = int(self.target_year.get().strip())
        return validate_date(year, month, day)

    def calculate_with_animation(self) -> None:
        self.error_label.config(text="")
        if self.animation_job:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None

        try:
            dob = self._get_dob()
            target = self._get_target_date()
            res = calculate_age(dob, target)

            self.placeholder_frame.pack_forget()
            self.results_content_frame.pack(fill="both", expand=True)

            self.bday_banner.pack_forget()
            if res["is_birthday_today"]:
                self.bday_banner.pack(fill="x", pady=(0, 8))

            bday_text = (
                "Today! 🎂"
                if res["is_birthday_today"]
                else f"{res['next_birthday'].strftime('%d %b %Y')} ({res['days_until_next_birthday']}d left)"
            )
            self.lbl_next_bday.config(text=bday_text)

            leap_str = "Leap Year Baby" if res["is_leap_year_born"] else "Standard Year"
            self.lbl_birth_info.config(text=f"{res['day_of_week']} • {leap_str}")

            target_years = res["years"]
            target_months = res["months"]
            target_days = res["days"]
            target_total_days = res["total_days"]
            target_hours = res["total_hours"]

            total_steps = 18
            interval_ms = 22

            def step_animation(current_step: int = 0):
                if current_step <= total_steps:
                    progress = current_step / total_steps
                    ease = 1.0 - (1.0 - progress) ** 3

                    curr_y = int(target_years * ease)
                    curr_m = int(target_months * ease)
                    curr_d = int(target_days * ease)
                    curr_td = int(target_total_days * ease)
                    curr_th = int(target_hours * ease)

                    self.val_years.config(text=str(curr_y))
                    self.val_months.config(text=str(curr_m))
                    self.val_days.config(text=str(curr_d))
                    self.lbl_days_total.config(text=f"{curr_td:,} days")
                    self.lbl_total_hours.config(text=f"{curr_th:,} hrs")
                    self.lbl_age_summary.config(text=f"{curr_y} Years, {curr_m} Months, {curr_d} Days")

                    self.animation_job = self.root.after(interval_ms, lambda: step_animation(current_step + 1))
                else:
                    self.val_years.config(text=str(target_years))
                    self.val_months.config(text=str(target_months))
                    self.val_days.config(text=str(target_days))
                    self.lbl_days_total.config(text=f"{target_total_days:,} days ({res['total_weeks']:,} wks)")
                    self.lbl_total_hours.config(text=f"{target_hours:,} hrs")
                    self.lbl_age_summary.config(text=f"{target_years} Years, {target_months} Months, {target_days} Days")
                    self.animation_job = None

            step_animation(0)

        except ValueError as err:
            self.error_label.config(text=f"⚠️ {err}")

    def reset(self) -> None:
        if self.animation_job:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None

        today = date.today()
        self.dob_day.set(str(today.day))
        self.dob_month.set(calendar.month_name[today.month])
        self.dob_year.set("2000")

        self._set_target_mode("today")
        self.error_label.config(text="")
        self.bday_banner.pack_forget()

        self.results_content_frame.pack_forget()
        self.placeholder_frame.pack(fill="both", expand=True)


def launch_gui() -> None:
    root = tk.Tk()
    app = AgeCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
