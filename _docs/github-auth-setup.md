# GitHub Authentication Setup Guide

This guide will help you set up GitHub OAuth authentication for your MCP server.

## Overview

The authentication system allows users to:
- Login with their GitHub account
- Access protected MCP tools and resources
- View their GitHub profile information
- Logout and manage sessions

## Features

- 🔐 **Secure OAuth 2.0 Flow**: Industry-standard GitHub OAuth implementation
- 🛡️ **CSRF Protection**: State parameter validation
- 📦 **Session Management**: In-memory session storage (easily extensible to Redis/Database)
- 🎨 **Beautiful UI**: Modern web interface for OAuth callbacks
- 🔧 **MCP Tools**: Native tools for login, logout, and status checks
- 📚 **MCP Resources**: Access user profile and session information
- 🚀 **Easy Integration**: Follows your existing MCP component structure

## Setup Instructions

### Step 1: Create a GitHub OAuth App

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click **"New OAuth App"** or **"New GitHub App"**
3. Fill in the application details:
   - **Application name**: Your MCP Server Name (e.g., "Cox's Bazar MCP Server")
   - **Homepage URL**: `http://localhost:8000` (or your server URL)
   - **Application description**: (Optional) A brief description
   - **Authorization callback URL**: `http://localhost:8000/auth/callback`
4. Click **"Register application"**
5. Copy your **Client ID** and generate a new **Client Secret**

### Step 2: Configure Environment Variables

Create or update your `.env` file in the project root:

```bash
# GitHub OAuth Configuration
GITHUB_CLIENT_ID=your_client_id_here
GITHUB_CLIENT_SECRET=your_client_secret_here
GITHUB_REDIRECT_URI=http://localhost:8000/auth/callback

# MCP Server Configuration
TRANSPORT_NAME=sse
PORT=8000
```

**Important Notes:**
- Keep your `GITHUB_CLIENT_SECRET` secure and never commit it to version control
- Add `.env` to your `.gitignore` file
- For production, use environment-specific URLs (e.g., `https://yourdomain.com/auth/callback`)

### Step 3: Install Dependencies

The authentication system requires `httpx` for async HTTP requests. Install dependencies:

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### Step 4: Run the Server

Start your MCP server with SSE or streamable-http transport (required for web routes):

```bash
# Using the command
cox-mcp-server

# Or directly with Python
python src/mcp_server/server.py
```

The server should output:
```
✅ Registered tool: auth
✅ Registered resource: auth_user
✅ Registered project custom routes
✅ Registered auth routes (transport: sse)
```

### Step 5: Verify Configuration

You can verify your configuration using the MCP tool:

```bash
# Call the github_config_check tool
# This will show your configuration status
```

Or visit the web interface at: `http://localhost:8000`

## Usage

### Using MCP Tools

#### 1. Check Configuration

```python
# Call: github_config_check
# Returns: Configuration status and setup instructions if not configured
```

#### 2. Login with GitHub

```python
# Call: github_login
# Returns: Authorization URL to visit in your browser
```

**Flow:**
1. Call the `github_login` tool
2. Visit the provided URL in your browser
3. Authorize the application on GitHub
4. You'll be redirected to the callback page
5. Session is created and stored

#### 3. Check Authentication Status

```python
# Call: github_auth_status
# Returns: Current user information and session details
```

#### 4. Logout

```python
# Call: github_logout
# Returns: Confirmation of successful logout
```

### Using Web Interface

When running with SSE/HTTP transport, you can use the web interface:

1. **Login**: Visit `http://localhost:8000/auth/login`
2. **View Status**: Visit `http://localhost:8000/auth/status`
3. **Logout**: Visit `http://localhost:8000/auth/logout`

### Using MCP Resources

#### Get User Profile

```python
# Resource URI: auth://user/profile
# Returns: JSON with user profile information
```

#### Get Session Info

```python
# Resource URI: auth://session/info
# Returns: JSON with session information (without sensitive tokens)
```

## Protecting Your Tools/Resources

You can protect your MCP tools and resources with the `@require_auth` decorator:

```python
from mcp_server.mcp_instance import mcp
from mcp.server.fastmcp import Context
from mcp_server.utils.auth_helpers import require_auth

@mcp.tool()
@require_auth
async def protected_tool(ctx: Context) -> str:
    """
    This tool requires authentication.
    """
    # Your protected logic here
    return "Protected content - user is authenticated!"
```

If a user is not authenticated, they'll receive:
```
❌ Authentication required. Please login with GitHub first using the 'github_login' tool.
```

## Architecture

### Components Structure

```
src/mcp_server/
├── components/
│   ├── tools/
│   │   └── auth.py              # Authentication tools
│   └── resources/
│       └── auth_user.py         # User info resources
├── config/
│   ├── project_custom_routes.py # Project routes
│   └── auth_routes.py           # OAuth callback routes
├── models/
│   ├── auth_models.py           # GitHubUser, AuthSession models
│   └── itinerary_models.py
└── utils/
    ├── auth_helpers.py          # OAuth helpers, session management
    └── register_mcp_components.py
```

### Authentication Flow

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       │ 1. Call github_login
       ▼
┌─────────────────────┐
│  MCP Tool (auth.py) │
└──────┬──────────────┘
       │
       │ 2. Generate auth URL
       ▼
┌────────────────────────┐
│  Browser (GitHub)      │
│  User authorizes app   │
└──────┬─────────────────┘
       │
       │ 3. Redirect with code
       ▼
┌──────────────────────────┐
│  /auth/callback route    │
└──────┬───────────────────┘
       │
       │ 4. Exchange code for token
       ▼
┌──────────────────────────┐
│  GitHub API              │
│  Get user info           │
└──────┬───────────────────┘
       │
       │ 5. Create session
       ▼
┌──────────────────────────┐
│  Session Store           │
│  Store user + token      │
└──────┬───────────────────┘
       │
       │ 6. Success page
       ▼
┌─────────────┐
│   User      │
│   (Logged in)│
└─────────────┘
```

### Session Management

**Current Implementation:**
- In-memory session storage (dictionary)
- Sessions stored with secure random IDs
- State validation for CSRF protection

**Production Recommendations:**
- Use Redis for distributed session storage
- Implement session expiration (TTL)
- Add refresh token support
- Consider JWT for stateless authentication

### Security Features

1. **CSRF Protection**: State parameter validation
2. **Secure Tokens**: Using `secrets.token_urlsafe()` for session IDs
3. **Token Privacy**: Access tokens never exposed in responses
4. **HTTPS Requirement**: Should use HTTPS in production
5. **Scope Limitation**: Only requests necessary scopes (`read:user`, `user:email`)

## Extending the Auth System

### Add More OAuth Providers

You can add more OAuth providers (Google, Microsoft, etc.) by:

1. Creating new helper functions in `utils/auth_helpers.py`
2. Adding new tools in `components/tools/auth.py`
3. Adding new callback routes in `config/auth_routes.py`

### Add Database Storage

Replace in-memory storage with database:

```python
# Example with SQLAlchemy
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Session(Base):
    __tablename__ = 'sessions'
    
    id = Column(String, primary_key=True)
    access_token = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    # ... more fields

# Update get_session, create_session, delete_session functions
```

### Add Role-Based Access Control (RBAC)

```python
# In auth_helpers.py
def require_role(role: str):
    """Decorator to require specific role."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            session = get_current_session()
            if not session or role not in session.user.roles:
                return f"❌ Requires {role} role"
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@mcp.tool()
@require_role("admin")
async def admin_tool(ctx: Context) -> str:
    return "Admin-only content"
```

## Troubleshooting

### Configuration Errors

**Issue**: `Missing GitHub OAuth configuration`

**Solution**: 
- Verify `.env` file exists and contains all three variables
- Check that `.env` is in the project root
- Restart the server after updating `.env`

### Callback Errors

**Issue**: "Invalid or Expired State"

**Solution**:
- This happens if you wait too long (>10 minutes) between starting login and completing it
- Start the login process again

**Issue**: "Invalid redirect_uri"

**Solution**:
- Ensure `GITHUB_REDIRECT_URI` matches exactly what you configured in GitHub OAuth App
- Check for trailing slashes
- Verify the port number matches your server

### Session Errors

**Issue**: Session lost after server restart

**Solution**:
- This is expected with in-memory storage
- For persistent sessions, implement database storage or Redis

### Transport Errors

**Issue**: Auth routes not working

**Solution**:
- Ensure you're using SSE or streamable-http transport (not stdio)
- Check that `TRANSPORT_NAME` in `.env` is set to `sse` or `streamable-http`
- Verify the auth routes are being registered (check server logs)

## Examples

### Example 1: Basic Authentication Flow

```python
# 1. Check config
response = await mcp.call_tool("github_config_check")
print(response)
# ✅ GitHub OAuth Configuration...

# 2. Login
response = await mcp.call_tool("github_login")
print(response)
# Visit: https://github.com/login/oauth/authorize?...

# 3. [User authorizes in browser]

# 4. Check status
response = await mcp.call_tool("github_auth_status")
print(response)
# ✅ Authenticated with GitHub
# Username: @your_username
# ...
```

### Example 2: Protected Resource

```python
from mcp_server.mcp_instance import mcp
from mcp.server.fastmcp import Context
from mcp_server.utils.auth_helpers import require_auth, get_current_session

@mcp.tool()
@require_auth
async def get_user_repos(ctx: Context) -> str:
    """Get authenticated user's GitHub repositories."""
    session = get_current_session()
    
    # Use the access token to call GitHub API
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/repos",
            headers={
                "Authorization": f"Bearer {session.access_token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        repos = response.json()
        
    return f"Found {len(repos)} repositories"
```

## Testing

### Test Authentication Flow

1. Start server: `cox-mcp-server`
2. Open browser: `http://localhost:8000`
3. Click login link: `http://localhost:8000/auth/login`
4. Authorize on GitHub
5. Verify success page shows your profile
6. Check status: `http://localhost:8000/auth/status`
7. Test logout: `http://localhost:8000/auth/logout`

### Test with MCP Client

If using with Cursor or another MCP client:

1. Ensure transport is set correctly
2. Call `github_config_check` to verify setup
3. Call `github_login` and follow instructions
4. Call `github_auth_status` to verify login
5. Test protected tools

## Best Practices

1. **Never commit secrets**: Always use environment variables
2. **Use HTTPS in production**: Protect tokens in transit
3. **Implement token refresh**: For long-lived sessions
4. **Add rate limiting**: Prevent abuse of auth endpoints
5. **Log auth events**: Track logins, logouts, and failures
6. **Implement session expiration**: Set reasonable TTLs
7. **Validate redirect URIs**: Prevent open redirect vulnerabilities
8. **Use database storage**: For production deployments
9. **Add monitoring**: Track auth success/failure rates
10. **Test thoroughly**: Verify all edge cases and error conditions

## Resources

- [GitHub OAuth Documentation](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps)
- [OAuth 2.0 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your `.env` configuration
3. Check server logs for error messages
4. Review GitHub OAuth app settings
5. Test with the web interface first before MCP clients

## License

This authentication system is part of your MCP server project and follows the same license.

