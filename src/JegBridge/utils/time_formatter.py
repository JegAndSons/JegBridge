from datetime import datetime

class TimeFormatter:
    """
    A class to format datetime strings for various use cases.
    """

    def __init__(self, dt: datetime = None):
        """
        Initialize the TimeFormatter with a specific datetime.
        If no datetime is provided, use the current datetime.
        """
        self._datetime = dt or datetime.now()

    @property
    def iso_format(self) -> str:
        """
        Returns the datetime in ISO 8601 format (e.g., '2025-01-15T13:45:30').
        """
        return self._datetime.isoformat()

    def format(self, format_string: str) -> str:
        """
        Returns the datetime formatted with a user-defined format string.
        :param format_string: A strftime-compatible format string.
        :return: The formatted datetime string.
        """
        return self._datetime.strftime(format_string)

    def update_datetime(self, new_dt: datetime):
        """
        Updates the internal datetime to a new value.
        """
        self._datetime = new_dt

    @property
    def amazon_auth_format(self) -> str:
        """
        Returns the datetime in a formatted how amazons auth api needs it (E.G. 2025-01-15 18:37:38.719447)
        """
        return self._datetime.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    
    # Example Usage
    formatter = TimeFormatter()

    print(formatter._datetime)
