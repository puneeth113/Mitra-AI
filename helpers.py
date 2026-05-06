# helpers.py

import re
from datetime import datetime


# ==========================================================
# ERP VALIDATION
# ==========================================================

def validate_erp(erp: str):
    """
    Validates ERP format:
    Must be 11 digits followed by _OIS
    Example: 20262002367_OIS
    """
    erp = erp.strip()

    if not re.fullmatch(r"\d{11}_OIS", erp):
        return False, "Invalid ERP format. Example: 20262002367_OIS"

    return True, ""


# ==========================================================
# TIME VALIDATION
# ==========================================================

def validate_time_fmt(time_str: str):
    """
    Validates time format HH:MM (24-hour)
    """
    try:
        datetime.strptime(time_str.strip(), "%H:%M")
        return True
    except Exception:
        return False


# ==========================================================
# HOURS CALCULATION
# ==========================================================

def calc_hours(start_time: str, end_time: str):
    """
    Calculates total hours between two times
    Returns float hours
    """
    try:
        start = datetime.strptime(start_time.strip(), "%H:%M")
        end = datetime.strptime(end_time.strip(), "%H:%M")

        diff = (end - start).total_seconds() / 3600
        return diff
    except Exception:
        return None


# ==========================================================
# ATTENDANCE EVALUATION
# ==========================================================

def eval_attendance(worked_hours: float, shift_info: dict):
    """
    Determines attendance status:
    - Full Day
    - Half Day
    - Insufficient
    """
    total_hours = shift_info.get("total", 8)
    half_day = total_hours / 2

    if worked_hours >= total_hours:
        return {
            "color": "success",
            "message": f"Full working day ({worked_hours:.2f}/{total_hours:.2f} hrs)."
        }

    elif worked_hours >= half_day:
        return {
            "color": "warning",
            "message": f"Half-day eligible ({worked_hours:.2f} hrs worked)."
        }

    else:
        return {
            "color": "error",
            "message": f"Insufficient hours ({worked_hours:.2f} hrs). Please contact HR."
        }


# ==========================================================
# OPTIONAL HELPER (GOOD FOR FUTURE)
# ==========================================================

def format_datetime_now(fmt="%d %B %Y"):
    """
    Returns current date in readable format
    """
    return datetime.now().strftime(fmt)