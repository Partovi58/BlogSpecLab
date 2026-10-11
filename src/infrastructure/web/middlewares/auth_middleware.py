from typing import Any, Dict

from src.domain.exceptions.post_exceptions import UnauthorizedException


class AuthContext:
    def __init__(self, user_id: str, is_authenticated: bool = True):
        self.user_id = user_id
        self.is_authenticated = is_authenticated


def extract_auth_context(headers: Dict[str, Any]) -> AuthContext:
    """Extracts author context from authorization header or mock token."""
    auth_header = headers.get("Authorization") or headers.get("authorization")
    if not auth_header:
        raise UnauthorizedException("Authentication token missing")

    # Supports format "Bearer <user_id>" or "User <user_id>"
    parts = auth_header.split()
    if len(parts) == 2:
        user_id = parts[1]
    else:
        user_id = auth_header.strip()

    if not user_id:
        raise UnauthorizedException("Invalid authentication token")

    return AuthContext(user_id=user_id, is_authenticated=True)
