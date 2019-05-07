class InvalidScope(Exception):
    def __init__(self, message="Cannot process scope in invalid form", **kwargs):
        super().__init__(message, **kwargs)


class OverrideError(Exception):
    def __init__(
        self, message="Override methods must return a boolean value", **kwargs
    ):
        super().__init__(message, **kwargs)
