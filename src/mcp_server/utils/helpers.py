"""Helper utility functions."""

import os
from collections.abc import Callable
from datetime import UTC, datetime

import requests
from dateutil import parser
from dotenv import load_dotenv
from fastmcp.server.auth import AuthContext
from fastmcp.server.dependencies import get_context, get_http_headers, get_http_request

load_dotenv()

MAX_TRIP_DAYS = 14
TEMP_COOL = 20
TEMP_PLEASANT = 25
TEMP_WARM = 30
TEMP_HOT = 35
HTTP_TIMEOUT_SECONDS = 100


def format_date(date_str: str) -> str:
    """
    Format date string to standard format.

    Args:
        date_str: Input date string

    Returns:
        Formatted date string (DD MMM YYYY)

    """
    try:
        dt = datetime.now(tz=UTC) if date_str.lower() == "today" else parser.parse(date_str)
        return dt.strftime("%d %b %Y")
    except ValueError:
        return datetime.now(tz=UTC).strftime("%d %b %Y")


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
    if days > MAX_TRIP_DAYS:
        return MAX_TRIP_DAYS
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

    if temp < TEMP_COOL:
        desc = "Cool"
    elif temp < TEMP_PLEASANT:
        desc = "Pleasant"
    elif temp < TEMP_WARM:
        desc = "Warm"
    elif temp < TEMP_HOT:
        desc = "Hot"
    else:
        desc = "Very Hot"

    return f"{temp_str} ({desc})"


def require_permissions(*required: str) -> Callable[[AuthContext], bool]:
    """Return an auth checker that verifies the token's `permissions` claim."""
    required_set = set(required)

    def check(ctx: AuthContext) -> bool:
        if ctx.token is None:
            return False
        permissions = ctx.token.claims.get("permissions", [])
        return required_set.issubset(set(permissions))

    return check


def require_premium_user(ctx: AuthContext) -> bool:
    """Check for premium user status in token claims."""
    return ctx.token is not None


def get_client_ip() -> str:
    """Get the client IP address from the current HTTP request."""
    request = get_http_request()
    return request.client.host if request.client else "Unknown"


def get_user_agent() -> str:
    """Get the User-Agent header from the current HTTP request."""
    headers = get_http_headers()
    return headers.get("user-agent", "Unknown")


def get_mcp_client_name() -> str:
    """Get the MCP client name from the current session context."""
    ctx = get_context()
    return ctx.request_context.session.client_params.clientInfo.name or "Unknown"


def get_mcp_session_id() -> str:
    """Get the MCP session ID from the current context."""
    ctx = get_context()
    return ctx.session_id


def get_auth0_user_info(token: str) -> dict:
    """Fetch user info from Auth0 using the given bearer token."""
    auth0_domain = os.getenv("AUTH0_DOMAIN")
    url = f"https://{auth0_domain}/userinfo"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()
