class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


class TokenMissingError(AuthenticationError):
    """Raised when the access token is missing in the authentication response."""
    pass

