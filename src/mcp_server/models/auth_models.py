"""
Auth models for GitHub OAuth authentication.
"""
from typing import Optional
from datetime import datetime

class GitHubUser:
    """GitHub user model."""
    
    def __init__(
        self,
        id: int,
        login: str,
        name: Optional[str],
        email: Optional[str],
        avatar_url: str,
        bio: Optional[str] = None,
        location: Optional[str] = None,
        company: Optional[str] = None,
        created_at: Optional[str] = None,
    ):
        self.id = id
        self.login = login
        self.name = name
        self.email = email
        self.avatar_url = avatar_url
        self.bio = bio
        self.location = location
        self.company = company
        self.created_at = created_at
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "login": self.login,
            "name": self.name,
            "email": self.email,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "location": self.location,
            "company": self.company,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_github_api(cls, data: dict):
        """Create from GitHub API response."""
        return cls(
            id=data.get("id"),
            login=data.get("login"),
            name=data.get("name"),
            email=data.get("email"),
            avatar_url=data.get("avatar_url"),
            bio=data.get("bio"),
            location=data.get("location"),
            company=data.get("company"),
            created_at=data.get("created_at"),
        )


class AuthSession:
    """Authentication session model."""
    
    def __init__(
        self,
        access_token: str,
        token_type: str,
        scope: str,
        user: GitHubUser,
        created_at: Optional[datetime] = None,
    ):
        self.access_token = access_token
        self.token_type = token_type
        self.scope = scope
        self.user = user
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "scope": self.scope,
            "user": self.user.to_dict(),
            "created_at": self.created_at.isoformat(),
        }
    
    def is_valid(self) -> bool:
        """Check if session is valid."""
        return bool(self.access_token and self.user)

