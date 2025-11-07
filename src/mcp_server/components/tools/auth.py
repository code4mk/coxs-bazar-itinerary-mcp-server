"""
Authentication tools for GitHub OAuth.
"""
from mcp_server.mcp_instance import mcp
from mcp.server.fastmcp import Context
from mcp_server.utils.auth_helpers import (
    get_authorization_url,
    get_current_session,
    delete_all_sessions,
    get_github_config,
    _sessions,
)


@mcp.tool()
async def github_login(ctx: Context) -> str:
    """
    Initiate GitHub OAuth login flow.
    
    Returns:
        Instructions with authorization URL for the user to visit
    """
    try:
        # Check if already logged in
        session = get_current_session()
        if session and session.is_valid():
            return f"""✅ Already logged in as @{session.user.login}
            
User Details:
- Name: {session.user.name or 'N/A'}
- Email: {session.user.email or 'N/A'}
- GitHub: https://github.com/{session.user.login}

To logout, use the 'github_logout' tool.
"""
        
        # Generate authorization URL to validate configuration
        get_authorization_url()
        
        return """🔐 GitHub Authentication Required

To use protected tools, please authenticate with GitHub:

http://localhost:8000/auth/login

**Steps:**
1. Click the URL above or copy it to your browser
2. Authorize the application on GitHub
3. You'll be redirected back automatically
4. Return here and run your tool again

Once authenticated, you'll have access to all protected features!
"""
    except ValueError as e:
        return f"""❌ Configuration Error

{str(e)}

Please set the required environment variables in your .env file or environment.
"""
    except Exception as e:
        return f"❌ Error initiating login: {str(e)}"


@mcp.tool()
async def github_logout(ctx: Context) -> str:
    """
    Logout from GitHub (clear all sessions).
    
    Returns:
        Confirmation message
    """
    try:
        session = get_current_session()
        if not session:
            return "ℹ️  Not currently logged in."
        
        # Get user info before deleting
        username = session.user.login
        
        # Delete ALL sessions from store (not just clear pointer)
        count = delete_all_sessions()
        
        return f"""✅ Successfully logged out @{username}

Cleared {count} session(s) from the store.
You will need to login again to access protected tools."""
    except Exception as e:
        return f"❌ Error during logout: {str(e)}"


@mcp.tool()
async def github_auth_status(ctx: Context) -> str:
    """
    Check current GitHub authentication status.
    
    Returns:
        Current authentication status and user information if logged in
    """
    try:
        session = get_current_session()
        
        if not session or not session.is_valid():
            return """🔓 Not Authenticated

Use the 'github_login' tool to authenticate with GitHub.
"""
        
        user = session.user
        
        return f"""✅ Authenticated with GitHub

**User Information:**
- Username: @{user.login}
- Name: {user.name or 'N/A'}
- Email: {user.email or 'N/A'}
- Bio: {user.bio or 'N/A'}
- Location: {user.location or 'N/A'}
- Company: {user.company or 'N/A'}
- Avatar: {user.avatar_url}
- Profile: https://github.com/{user.login}
- Member since: {user.created_at or 'N/A'}

**Session Information:**
- Token Type: {session.token_type}
- Scope: {session.scope}
- Authenticated at: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}
"""
    except Exception as e:
        return f"❌ Error checking status: {str(e)}"


@mcp.tool()
async def github_config_check(ctx: Context) -> str:
    """
    Check if GitHub OAuth is properly configured.
    
    Returns:
        Configuration status
    """
    try:
        config = get_github_config()
        
        return f"""✅ GitHub OAuth Configuration

**Client ID:** {config['client_id'][:8]}...{config['client_id'][-4:]}
**Client Secret:** {'*' * 8} (hidden)
**Redirect URI:** {config['redirect_uri']}

Configuration is valid! You can use the 'github_login' tool to authenticate.
"""
    except ValueError as e:
        return f"""❌ Configuration Error

{str(e)}

**Setup Instructions:**

1. Create a GitHub OAuth App:
   - Go to: https://github.com/settings/developers
   - Click "New OAuth App"
   - Fill in the details:
     * Application name: Your MCP Server Name
     * Homepage URL: http://localhost:8000
     * Authorization callback URL: http://localhost:8000/auth/callback

2. Set environment variables in your .env file:
   ```
   GITHUB_CLIENT_ID=your_client_id
   GITHUB_CLIENT_SECRET=your_client_secret
   GITHUB_REDIRECT_URI=http://localhost:8000/auth/callback
   ```

3. Restart your MCP server
"""
    except Exception as e:
        return f"❌ Error checking configuration: {str(e)}"


@mcp.tool()
async def github_debug_sessions(ctx: Context) -> str:
    """
    Debug tool: Show all active sessions and current session info.
    Useful for troubleshooting authentication issues.
    
    Returns:
        Debug information about sessions
    """
    try:
        output = "🔍 **GitHub Auth Debug Information**\n\n"
        
        # Show total sessions
        output += f"**Total Active Sessions:** {len(_sessions)}\n\n"
        
        if not _sessions:
            output += "No active sessions found.\n"
            output += "Use 'github_login' to authenticate.\n"
            return output
        
        # Show all sessions
        output += "**All Sessions:**\n"
        for idx, (session_id, session) in enumerate(_sessions.items(), 1):
            output += f"\n{idx}. Session ID: `{session_id[:16]}...`\n"
            output += f"   - User: @{session.user.login}\n"
            output += f"   - Name: {session.user.name or 'N/A'}\n"
            output += f"   - Created: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            output += f"   - Valid: {'✅ Yes' if session.is_valid() else '❌ No'}\n"
        
        # Show current session
        output += "\n**Current Session:**\n"
        current = get_current_session()
        if current:
            output += f"✅ Active session for @{current.user.login}\n"
            output += f"   Created: {current.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        else:
            output += "❌ No current session active\n"
        
        return output
    except Exception as e:
        return f"❌ Error getting debug info: {str(e)}"

