class NmppError(Exception):
    """Base application exception."""


class AuthenticationError(NmppError):
    """Raised for authentication or authorization failures."""


class EntityNotFoundError(NmppError):
    """Raised when an entity cannot be found."""


class ValidationError(NmppError):
    """Raised when business validation fails."""
