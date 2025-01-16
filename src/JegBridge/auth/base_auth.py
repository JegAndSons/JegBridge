from abc import ABC, abstractmethod

class BaseAuth(ABC):
    """
    Abstract base class for authentication mechanisms.
    """
    def __init__(self, use_production: bool = False, sandbox_url: str = None, production_url: str = None):
        """
        Initialize the authentication object.

        Args:
            use_production (bool): Whether to use the production environment. Defaults to False (sandbox).
            sandbox_url (str): Optional custom sandbox URL.
            production_url (str): Optional custom production URL.
        """
        self.use_production = use_production
        self._sandbox_url = sandbox_url
        self._production_url = production_url

    @property
    def base_url(self) -> str:
        """
        Get the appropriate base URL based on the environment.

        Returns:
            str: The base URL.
        """
        if self.use_production and self._production_url:
            return self._production_url
        if not self.use_production and self._sandbox_url:
            return self._sandbox_url
        raise ValueError("Sandbox or production URL not configured.")

    @abstractmethod
    def authenticate(self) -> None:
        """
        Perform the necessary authentication flow to retrieve credentials.
        """
        pass

    @abstractmethod
    def get_headers(self) -> dict:
        """
        Return authentication headers for API requests.

        Returns:
            dict: A dictionary containing headers (e.g., Authorization tokens).
        """
        pass
