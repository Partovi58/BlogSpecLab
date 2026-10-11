class PostException(Exception):
    """Base exception for Post domain errors."""
    pass


class InvalidPayloadException(PostException):
    """Raised when post payload (title or content) is empty or whitespace only."""
    pass


class UnauthorizedException(PostException):
    """Raised when user is not authorized to edit or publish a post."""
    pass


class ImmutablePostException(PostException):
    """Raised when an operation attempts to modify or revert a published post."""
    pass


class PostNotFoundException(PostException):
    """Raised when a post cannot be found."""
    pass
