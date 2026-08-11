class RepositoryCloneError(Exception):
    """Raised when a repository cannot be cloned."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
