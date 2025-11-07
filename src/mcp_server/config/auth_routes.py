"""
Authentication routes for GitHub OAuth flow.
These routes are only registered when transport is not stdio.
"""
from mcp_server.mcp_instance import mcp
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from mcp_server.utils.auth_helpers import (
    validate_state,
    exchange_code_for_token,
    get_github_user,
    create_session,
    set_current_session,
    get_current_session,
)


@mcp.custom_route("/auth/login", methods=["GET"])
async def auth_login(request: Request):
    """
    Redirect to GitHub OAuth authorization page.
    """
    from mcp_server.utils.auth_helpers import get_authorization_url
    
    try:
        auth_data = get_authorization_url()
        return RedirectResponse(url=auth_data['url'])
    except Exception as e:
        return HTMLResponse(
            content=f"""
            <html>
                <head><title>Login Error</title></head>
                <body>
                    <h1>❌ Configuration Error</h1>
                    <p>{str(e)}</p>
                    <p>Please check your GitHub OAuth configuration.</p>
                </body>
            </html>
            """,
            status_code=500
        )


@mcp.custom_route("/auth/callback", methods=["GET"])
async def auth_callback(request: Request):
    """
    GitHub OAuth callback endpoint.
    Handles the redirect from GitHub after user authorization.
    """
    # Get code and state from query parameters
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    error = request.query_params.get("error")
    
    # Handle error from GitHub
    if error:
        error_description = request.query_params.get("error_description", error)
        return HTMLResponse(
            content=f"""
            <html>
                <head><title>Authentication Error</title></head>
                <body style="font-family: system-ui; max-width: 600px; margin: 50px auto; padding: 20px;">
                    <h1>❌ Authentication Failed</h1>
                    <p><strong>Error:</strong> {error}</p>
                    <p><strong>Description:</strong> {error_description}</p>
                    <br>
                    <a href="/auth/login" style="background: #0366d6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px;">Try Again</a>
                </body>
            </html>
            """,
            status_code=400
        )
    
    # Validate required parameters
    if not code or not state:
        return HTMLResponse(
            content="""
            <html>
                <head><title>Invalid Request</title></head>
                <body style="font-family: system-ui; max-width: 600px; margin: 50px auto; padding: 20px;">
                    <h1>❌ Invalid Request</h1>
                    <p>Missing required parameters (code or state).</p>
                    <a href="/auth/login" style="background: #0366d6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px;">Try Again</a>
                </body>
            </html>
            """,
            status_code=400
        )
    
    # Validate state (CSRF protection)
    if not validate_state(state):
        return HTMLResponse(
            content="""
            <html>
                <head><title>Invalid State</title></head>
                <body style="font-family: system-ui; max-width: 600px; margin: 50px auto; padding: 20px;">
                    <h1>❌ Invalid or Expired State</h1>
                    <p>The authentication state is invalid or has expired. This could be a CSRF attack attempt.</p>
                    <a href="/auth/login" style="background: #0366d6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px;">Try Again</a>
                </body>
            </html>
            """,
            status_code=400
        )
    
    try:
        # Exchange code for access token
        access_token = await exchange_code_for_token(code)
        
        # Get user information
        user = await get_github_user(access_token)
        
        # Create session
        session_id = create_session(
            access_token=access_token,
            token_type="bearer",
            scope="read:user user:email",
            user=user,
        )
        
        # Set as current session
        set_current_session(session_id)
        
        # Return success page
        return HTMLResponse(
            content=f"""
            <html>
                <head>
                    <title>Authentication Successful</title>
                    <style>
                        body {{
                            font-family: system-ui, -apple-system, sans-serif;
                            max-width: 600px;
                            margin: 50px auto;
                            padding: 20px;
                            line-height: 1.6;
                        }}
                        .success {{
                            background: #d4edda;
                            border: 1px solid #c3e6cb;
                            color: #155724;
                            padding: 20px;
                            border-radius: 8px;
                            margin-bottom: 20px;
                        }}
                        .user-card {{
                            background: #f6f8fa;
                            border: 1px solid #d1d5da;
                            border-radius: 8px;
                            padding: 20px;
                            display: flex;
                            align-items: center;
                            gap: 20px;
                        }}
                        .avatar {{
                            border-radius: 50%;
                            width: 80px;
                            height: 80px;
                        }}
                        .user-info {{
                            flex: 1;
                        }}
                        .btn {{
                            display: inline-block;
                            background: #0366d6;
                            color: white;
                            padding: 10px 20px;
                            text-decoration: none;
                            border-radius: 6px;
                            margin-top: 20px;
                        }}
                        .session-info {{
                            background: #fff3cd;
                            border: 1px solid #ffeaa7;
                            padding: 15px;
                            border-radius: 6px;
                            margin-top: 20px;
                            font-size: 14px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="success">
                        <h1>✅ Authentication Successful!</h1>
                        <p>You have successfully authenticated with GitHub.</p>
                    </div>
                    
                    <div class="user-card">
                        <img src="{user.avatar_url}" alt="Avatar" class="avatar">
                        <div class="user-info">
                            <h2>@{user.login}</h2>
                            <p><strong>Name:</strong> {user.name or 'N/A'}</p>
                            <p><strong>Email:</strong> {user.email or 'N/A'}</p>
                            {f'<p><strong>Location:</strong> {user.location}</p>' if user.location else ''}
                            {f'<p><strong>Company:</strong> {user.company}</p>' if user.company else ''}
                        </div>
                    </div>
                    
                    <div class="session-info">
                        <strong>📋 Session Information:</strong><br>
                        Session ID: <code>{session_id[:16]}...{session_id[-8:]}</code>
                    </div>
                    
                    <a href="/auth/status" class="btn">View Full Status</a>
                    <a href="/" class="btn" style="background: #6c757d;">Go to Home</a>
                    
                    <p style="margin-top: 30px; color: #666; font-size: 14px;">
                        You can now close this window and use the MCP server with authentication.
                    </p>
                </body>
            </html>
            """
        )
    except Exception as e:
        return HTMLResponse(
            content=f"""
            <html>
                <head><title>Authentication Error</title></head>
                <body style="font-family: system-ui; max-width: 600px; margin: 50px auto; padding: 20px;">
                    <h1>❌ Authentication Error</h1>
                    <p><strong>Error:</strong> {str(e)}</p>
                    <br>
                    <a href="/auth/login" style="background: #0366d6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px;">Try Again</a>
                </body>
            </html>
            """,
            status_code=500
        )


@mcp.custom_route("/auth/status", methods=["GET"])
async def auth_status(request: Request):
    """
    Display current authentication status.
    """
    session = get_current_session()
    
    if not session or not session.is_valid():
        return HTMLResponse(
            content="""
            <html>
                <head><title>Authentication Status</title></head>
                <body style="font-family: system-ui; max-width: 600px; margin: 50px auto; padding: 20px;">
                    <h1>🔓 Not Authenticated</h1>
                    <p>You are not currently authenticated.</p>
                    <a href="/auth/login" style="background: #0366d6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px;">Login with GitHub</a>
                </body>
            </html>
            """
        )
    
    user = session.user
    
    return HTMLResponse(
        content=f"""
        <html>
            <head>
                <title>Authentication Status</title>
                <style>
                    body {{
                        font-family: system-ui, -apple-system, sans-serif;
                        max-width: 700px;
                        margin: 50px auto;
                        padding: 20px;
                        line-height: 1.6;
                    }}
                    .status {{
                        background: #d4edda;
                        border: 1px solid #c3e6cb;
                        color: #155724;
                        padding: 20px;
                        border-radius: 8px;
                        margin-bottom: 20px;
                    }}
                    .user-card {{
                        background: #f6f8fa;
                        border: 1px solid #d1d5da;
                        border-radius: 8px;
                        padding: 20px;
                        display: flex;
                        gap: 20px;
                        margin-bottom: 20px;
                    }}
                    .avatar {{
                        border-radius: 50%;
                        width: 100px;
                        height: 100px;
                    }}
                    .info-table {{
                        width: 100%;
                        border-collapse: collapse;
                    }}
                    .info-table td {{
                        padding: 8px;
                        border-bottom: 1px solid #e1e4e8;
                    }}
                    .info-table td:first-child {{
                        font-weight: bold;
                        width: 150px;
                    }}
                    .btn {{
                        display: inline-block;
                        background: #dc3545;
                        color: white;
                        padding: 10px 20px;
                        text-decoration: none;
                        border-radius: 6px;
                        margin-right: 10px;
                    }}
                    .btn-secondary {{
                        background: #6c757d;
                    }}
                </style>
            </head>
            <body>
                <div class="status">
                    <h1>✅ Authenticated with GitHub</h1>
                </div>
                
                <div class="user-card">
                    <img src="{user.avatar_url}" alt="Avatar" class="avatar">
                    <div style="flex: 1;">
                        <h2>@{user.login}</h2>
                        <table class="info-table">
                            <tr>
                                <td>Name:</td>
                                <td>{user.name or 'N/A'}</td>
                            </tr>
                            <tr>
                                <td>Email:</td>
                                <td>{user.email or 'N/A'}</td>
                            </tr>
                            {f'<tr><td>Bio:</td><td>{user.bio}</td></tr>' if user.bio else ''}
                            {f'<tr><td>Location:</td><td>{user.location}</td></tr>' if user.location else ''}
                            {f'<tr><td>Company:</td><td>{user.company}</td></tr>' if user.company else ''}
                            <tr>
                                <td>GitHub Profile:</td>
                                <td><a href="https://github.com/{user.login}" target="_blank">View Profile</a></td>
                            </tr>
                            {f'<tr><td>Member Since:</td><td>{user.created_at}</td></tr>' if user.created_at else ''}
                        </table>
                    </div>
                </div>
                
                <h3>Session Information</h3>
                <table class="info-table">
                    <tr>
                        <td>Token Type:</td>
                        <td>{session.token_type}</td>
                    </tr>
                    <tr>
                        <td>Scope:</td>
                        <td>{session.scope}</td>
                    </tr>
                    <tr>
                        <td>Authenticated At:</td>
                        <td>{session.created_at.strftime('%Y-%m-%d %H:%M:%S')}</td>
                    </tr>
                </table>
                
                <div style="margin-top: 30px;">
                    <a href="/auth/logout" class="btn">Logout</a>
                    <a href="/" class="btn btn-secondary">Go to Home</a>
                </div>
            </body>
        </html>
        """
    )


@mcp.custom_route("/auth/logout", methods=["GET"])
async def auth_logout(request: Request):
    """
    Logout endpoint - deletes all sessions.
    """
    from mcp_server.utils.auth_helpers import delete_all_sessions
    
    session = get_current_session()
    username = session.user.login if session else "Unknown"
    
    # Delete all sessions from store
    delete_all_sessions()
    
    return HTMLResponse(
        content=f"""
        <html>
            <head>
                <title>Logged Out</title>
                <style>
                    body {{
                        font-family: system-ui, -apple-system, sans-serif;
                        max-width: 600px;
                        margin: 50px auto;
                        padding: 20px;
                        text-align: center;
                    }}
                    .success {{
                        background: #d4edda;
                        border: 1px solid #c3e6cb;
                        color: #155724;
                        padding: 30px;
                        border-radius: 8px;
                        margin-bottom: 20px;
                    }}
                    .btn {{
                        display: inline-block;
                        background: #0366d6;
                        color: white;
                        padding: 10px 20px;
                        text-decoration: none;
                        border-radius: 6px;
                        margin: 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="success">
                    <h1>✅ Successfully Logged Out</h1>
                    <p>You have been logged out from @{username}</p>
                </div>
                
                <a href="/auth/login" class="btn">Login Again</a>
                <a href="/" class="btn" style="background: #6c757d;">Go to Home</a>
            </body>
        </html>
        """
    )

