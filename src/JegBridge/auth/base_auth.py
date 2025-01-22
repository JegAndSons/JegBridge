import requests
from abc import ABC, abstractmethod
from typing import Callable, Optional, Dict
from JegBridge.utils.custom_exceptions import RequestError

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

    def make_request(
        self,
        method: str,
        endpoint: str,
        get_headers_callback: Optional[Callable[[], Dict[str, str]]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make an HTTP request with common error handling.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            endpoint (str): Endpoint relative to the base URL.
            get_headers_callback: Callable that returns headers dictionary. Defaults to `self.get_headers`.
            **kwargs: Additional arguments to pass to the `requests.request` method.

        Returns:
            dict: The response JSON as a dictionary.

        Raises:
            RequestError: If the request fails or returns a non-200 status code.
        """
        if get_headers_callback is None:
            get_headers_callback = self.get_headers
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Merge default headers with any headers passed in kwargs
        headers = kwargs.pop("headers", {})
        headers.update(get_headers_callback())

        try:
            response = requests.request(
                method=method.lower(),
                url=url,
                headers=headers,
                **kwargs,
            )
            return response

        except requests.exceptions.RequestException as e:
            raise RequestError(f"Request failed: {e}")
        except ValueError as e:
            raise RequestError(f"Failed to parse response JSON: {e}")
