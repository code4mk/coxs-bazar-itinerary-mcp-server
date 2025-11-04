"""Helper utility functions."""
from datetime import datetime
from dateutil import parser

def format_date(date_str: str) -> str:
    """
    Format date string to standard format.
    
    Args:
        date_str: Input date string
    
    Returns:
        Formatted date string (DD MMM YYYY)
    """
    try:
        if date_str.lower() == "today":
            dt = datetime.today()
        else:
            dt = parser.parse(date_str)
        return dt.strftime("%d %b %Y")
    except Exception:
        return datetime.today().strftime("%d %b %Y")

def validate_days(days: int) -> int:
    """
    Validate number of days is within reasonable range.
    
    Args:
        days: Number of days
    
    Returns:
        Validated number of days (1-14)
    """
    if days < 1:
        return 1
    elif days > 14:
        return 14
    return days

def format_temperature(temp: float) -> str:
    """
    Format temperature with appropriate description.
    
    Args:
        temp: Temperature in Celsius
    
    Returns:
        Formatted temperature string with description
    """
    temp_str = f"{temp:.1f}°C"
    
    if temp < 20:
        desc = "Cool"
    elif temp < 25:
        desc = "Pleasant"
    elif temp < 30:
        desc = "Warm"
    elif temp < 35:
        desc = "Hot"
    else:
        desc = "Very Hot"
    
    return f"{temp_str} ({desc})"


