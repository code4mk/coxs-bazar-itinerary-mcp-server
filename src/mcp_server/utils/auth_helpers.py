"""
Authentication helper functions for GitHub OAuth.
"""
import os
import secrets
from typing import Optional, Dict, Any
from datetime import datetime
from functools import wraps
import httpx
from mcp_server.models.auth_models import GitHubUser, AuthSession


# In-memory session store (for production, use Redis or database)
_sessions: Dict[str, AuthSession] = {}
_state_store: Dict[str, Dict[str, Any]] = {}
_current_session_id: Optional[str] = None  # Track current active session


def get_github_config() -> Dict[str, str]:
    """
    Get GitHub OAuth configuration from environment variables.
    
    Required environment variables:
    - GITHUB_CLIENT_ID: GitHub OAuth App client ID
    - GITHUB_CLIENT_SECRET: GitHub OAuth App client secret
    - GITHUB_REDIRECT_URI: Callback URL (e.g., http://localhost:8000/auth/callback)
    """
    client_id = os.environ.get("GITHUB_CLIENT_ID")
    client_secret = os.environ.get("GITHUB_CLIENT_SECRET")
    redirect_uri = os.environ.get("GITHUB_REDIRECT_URI")
    
    if not all([client_id, client_secret, redirect_uri]):
        raise ValueError(
            "Missing GitHub OAuth configuration. Please set:\n"
            "- GITHUB_CLIENT_ID\n"
            "- GITHUB_CLIENT_SECRET\n"
            "- GITHUB_REDIRECT_URI"
        )
    
    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    }


def generate_state() -> str:
    """Generate a random state for CSRF protection."""
    return secrets.token_urlsafe(32)


def store_state(state: str, data: Optional[Dict[str, Any]] = None) -> None:
    """Store state with optional data."""
    _state_store[state] = {
        "created_at": datetime.now(),
        "data": data or {},
    }


def validate_state(state: str) -> bool:
    """Validate state and remove it from store."""
    if state in _state_store:
        # Check if state is not too old (e.g., 10 minutes)
        state_data = _state_store.pop(state)
        age = (datetime.now() - state_data["created_at"]).seconds
        return age < 600  # 10 minutes
    return False


def get_authorization_url() -> Dict[str, str]:
    """
    Generate GitHub authorization URL.
    
    Returns:
        Dictionary with 'url' and 'state' keys
    """
    config = get_github_config()
    state = generate_state()
    store_state(state)
    
    # GitHub OAuth scopes
    scopes = ["read:user", "user:email"]
    scope_string = " ".join(scopes)
    
    url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={config['client_id']}"
        f"&redirect_uri={config['redirect_uri']}"
        f"&scope={scope_string}"
        f"&state={state}"
    )
    
    return {
        "url": url,
        "state": state,
    }


async def exchange_code_for_token(code: str) -> str:
    """
    Exchange authorization code for access token.
    
    Args:
        code: Authorization code from GitHub
    
    Returns:
        Access token
    """
    config = get_github_config()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": config["client_id"],
                "client_secret": config["client_secret"],
                "code": code,
                "redirect_uri": config["redirect_uri"],
            },
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        data = response.json()
        
        if "error" in data:
            raise ValueError(f"GitHub OAuth error: {data.get('error_description', data['error'])}")
        
        return data["access_token"]


async def get_github_user(access_token: str) -> GitHubUser:
    """
    Get GitHub user information using access token.
    
    Args:
        access_token: GitHub access token
    
    Returns:
        GitHubUser object
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        response.raise_for_status()
        data = response.json()
        
        return GitHubUser.from_github_api(data)


def create_session(access_token: str, token_type: str, scope: str, user: GitHubUser) -> str:
    """
    Create a new authentication session.
    
    Args:
        access_token: GitHub access token
        token_type: Token type (usually "bearer")
        scope: OAuth scope
        user: GitHubUser object
    
    Returns:
        Session ID
    """
    session_id = secrets.token_urlsafe(32)
    session = AuthSession(
        access_token=access_token,
        token_type=token_type,
        scope=scope,
        user=user,
    )
    _sessions[session_id] = session
    return session_id


def get_session(session_id: str) -> Optional[AuthSession]:
    """Get session by ID."""
    return _sessions.get(session_id)


def delete_session(session_id: str) -> bool:
    """Delete session by ID."""
    if session_id in _sessions:
        del _sessions[session_id]
        return True
    return False


def get_current_session() -> Optional[AuthSession]:
    """
    Get current session.
    Returns the most recently authenticated session or None.
    """
    global _current_session_id
    
    # First check if we have a current session set
    if _current_session_id:
        session = get_session(_current_session_id)
        if session and session.is_valid():
            return session
    
    # If no current session or it's invalid, check environment variable (for compatibility)
    session_id = os.environ.get("MCP_SESSION_ID")
    if session_id:
        session = get_session(session_id)
        if session and session.is_valid():
            _current_session_id = session_id
            return session
    
    # As a fallback, return the most recent valid session
    if _sessions:
        # Get the most recently created session
        recent_session = max(_sessions.values(), key=lambda s: s.created_at)
        if recent_session.is_valid():
            _current_session_id = next(sid for sid, s in _sessions.items() if s == recent_session)
            return recent_session
    
    return None


def set_current_session(session_id: str) -> None:
    """Set current session ID."""
    global _current_session_id
    _current_session_id = session_id
    # Also set in environment for compatibility
    os.environ["MCP_SESSION_ID"] = session_id


def clear_current_session() -> None:
    """Clear current session."""
    global _current_session_id
    _current_session_id = None
    if "MCP_SESSION_ID" in os.environ:
        del os.environ["MCP_SESSION_ID"]


def delete_all_sessions() -> int:
    """
    Delete all sessions from the store.
    
    Returns:
        Number of sessions deleted
    """
    global _sessions, _current_session_id
    count = len(_sessions)
    _sessions.clear()
    _current_session_id = None
    if "MCP_SESSION_ID" in os.environ:
        del os.environ["MCP_SESSION_ID"]
    return count


def require_auth(func):
    """
    Decorator to require authentication for MCP tools/resources.
    
    Usage:
        @mcp.tool()
        @require_auth
        async def protected_tool(ctx: Context) -> str:
            return "Protected content"
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = get_current_session()
        
        # Debug info
        if not session:
            total_sessions = len(_sessions)
            if total_sessions > 0:
                return f"""❌ Authentication Error - Session Not Found

Debug Info:
- Total sessions in store: {total_sessions}
- Current session ID: {_current_session_id or 'None'}

This might be a session lookup issue. Try calling 'github_auth_status' to verify your session.
If you see your user info there but still get this error, please run 'github_debug_sessions' for more details.

To fix: Use 'github_login' tool to re-authenticate.
"""
            return "❌ Authentication required. Please login with GitHub first using the 'github_login' tool."
        
        if not session.is_valid():
            return f"""❌ Session Invalid

Your session exists but is marked as invalid.
- User: @{session.user.login if session.user else 'Unknown'}

Please use 'github_login' to re-authenticate.
"""
        
        return await func(*args, **kwargs)
    
    return wrapper

