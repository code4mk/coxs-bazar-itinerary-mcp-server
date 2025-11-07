# GitHub Authentication - Quick Start

This is a quick start guide to get GitHub authentication working in 5 minutes.

## 1. Create GitHub OAuth App (2 minutes)

1. Visit: https://github.com/settings/developers
2. Click "New OAuth App"
3. Fill in:
   - **Name**: Your MCP Server
   - **Homepage**: `http://localhost:8000`
   - **Callback**: `http://localhost:8000/auth/callback`
4. Click "Register"
5. Copy your **Client ID** and **Client Secret**

## 2. Configure Environment (1 minute)

Create `.env` file in project root:

```bash
# Transport (required for web routes)
TRANSPORT_NAME=sse
PORT=8000

# GitHub OAuth
GITHUB_CLIENT_ID=your_client_id_here
GITHUB_CLIENT_SECRET=your_client_secret_here
GITHUB_REDIRECT_URI=http://localhost:8000/auth/callback
```

## 3. Install Dependencies (1 minute)

```bash
uv sync
```

## 4. Start Server (30 seconds)

```bash
cox-mcp-server
```

You should see:
```
✅ Registered tool: auth
✅ Registered resource: auth_user
✅ Registered auth routes (transport: sse)
```

## 5. Test Authentication (30 seconds)

### Option A: Web Interface
1. Open browser: `http://localhost:8000/auth/login`
2. Authorize on GitHub
3. You'll see your profile!

### Option B: MCP Tools
1. Call tool: `github_login`
2. Copy URL and open in browser
3. Authorize on GitHub
4. Call tool: `github_auth_status` to verify

## Available Tools

| Tool | Description |
|------|-------------|
| `github_login` | Start login flow |
| `github_logout` | Logout current user |
| `github_auth_status` | Check login status |
| `github_config_check` | Verify configuration |

## Available Resources

| Resource | Description |
|----------|-------------|
| `auth://user/profile` | User profile (JSON) |
| `auth://session/info` | Session info (JSON) |

## Available Routes (Web UI)

| Route | Description |
|-------|-------------|
| `/auth/login` | Login page (redirects to GitHub) |
| `/auth/callback` | OAuth callback (automatic) |
| `/auth/status` | View current auth status |
| `/auth/logout` | Logout page |

## Protecting Your Tools

Add `@require_auth` decorator to protect tools:

```python
from mcp_server.utils.auth_helpers import require_auth

@mcp.tool()
@require_auth
async def protected_tool(ctx: Context) -> str:
    """This requires authentication."""
    return "Protected content!"
```

## Troubleshooting

### "Missing GitHub OAuth configuration"
- Check your `.env` file exists
- Verify all three variables are set
- Restart the server

### "Invalid redirect_uri"
- Ensure callback URL matches exactly in GitHub OAuth app
- Check for typos in `.env`

### Routes not working
- Make sure `TRANSPORT_NAME=sse` (not `stdio`)
- Check server logs for registration messages

## Next Steps

For detailed documentation, see:
- [Full Setup Guide](_docs/github-auth-setup.md)
- [Architecture Details](_docs/github-auth-setup.md#architecture)
- [Security Best Practices](_docs/github-auth-setup.md#security-features)

## Need Help?

1. Check configuration: Call `github_config_check` tool
2. Review server logs for error messages
3. Test with web interface first
4. See full documentation for advanced topics

