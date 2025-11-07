"""
Authentication resources for user information.
"""
from mcp_server.mcp_instance import mcp
from mcp_server.utils.auth_helpers import get_current_session
import json


@mcp.resource("auth://user/profile")
async def resource_user_profile() -> str:
    """
    Get current authenticated user's profile.
    
    Returns:
        JSON string with user profile data
    """
    session = get_current_session()
    
    if not session or not session.is_valid():
        return json.dumps({
            "error": "Not authenticated",
            "message": "Please login with GitHub using the 'github_login' tool"
        }, indent=2)
    
    return json.dumps(session.user.to_dict(), indent=2)


@mcp.resource("auth://session/info")
async def resource_session_info() -> str:
    """
    Get current session information (without sensitive tokens).
    
    Returns:
        JSON string with session data
    """
    session = get_current_session()
    
    if not session or not session.is_valid():
        return json.dumps({
            "authenticated": False,
            "message": "No active session"
        }, indent=2)
    
    return json.dumps({
        "authenticated": True,
        "token_type": session.token_type,
        "scope": session.scope,
        "user": {
            "username": session.user.login,
            "name": session.user.name,
            "avatar_url": session.user.avatar_url,
        },
        "created_at": session.created_at.isoformat(),
    }, indent=2)

