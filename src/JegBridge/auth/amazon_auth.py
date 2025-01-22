import requests
from typing import Optional
from datetime import datetime
from JegBridge.auth.base_auth import BaseAuth
from JegBridge.utils.custom_exceptions import TokenMissingError, AuthenticationError
from JegBridge.utils.time_formatter import TimeFormatter

class AmazonAuth(BaseAuth):
    """
    Amazon-specific authentication using OAuth2.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        refresh_token: str,
        use_production: bool = False,
        sandbox_url: str = None,
        production_url: str = None,
    ):
        """
        Initialize the AmazonAuth object.

        Args:
            client_id (str): Amazon client ID.
            client_secret (str): Amazon client secret.
            refresh_token (str): Refresh token for OAuth2.
            use_production (bool): Whether to use the production environment.
            sandbox_url (str): Optional custom sandbox URL.
            production_url (str): Optional custom production URL.
        """
        # Set marketplace-specific default URLs
        sandbox_url = sandbox_url or "https://sandbox.sellingpartnerapi-na.amazon.com/"
        production_url = production_url or "https://sellingpartnerapi-na.amazon.com/"

        super().__init__(use_production, sandbox_url, production_url)

        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token: Optional[str] = None

    def authenticate(self) -> dict:
        """
        Perform OAuth2 authentication to obtain an access token.

        Returns:
            dict: The full response JSON from the authentication API.

        Raises:
            AuthenticationError: If the authentication request fails or the response is invalid.
        """
        url = "https://api.amazon.com/auth/o2/token"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
            data = response.json()

            # Check if 'access_token' is present in the response
            self.access_token = data.get("access_token")
            if not self.access_token:
                raise TokenMissingError(
                    "Authentication succeeded but 'access_token' is missing in the response. "
                    "Check the API response format or credentials."
                )

        except requests.exceptions.RequestException as e:
            raise AuthenticationError(
                f"Failed to authenticate with Amazon API. Check your network connection, API URL, "
                f"or credentials. Details: {e}"
            )

        except ValueError as e:
            raise AuthenticationError(
                f"Failed to parse the authentication response as JSON. Ensure the API is returning valid JSON. "
                f"Details: {e}"
            )

    def get_headers(self) -> dict:
        """
        Get headers required for authenticated API requests.

        Returns:
            dict: A dictionary containing the 'Authorization' header.

        Raises:
            AuthenticationError: If the access token is missing or invalid.
        """
        self.authenticate()

        # Ensure the access token exists before returning headers
        if not self.access_token:
            raise AuthenticationError(
                "Unable to retrieve access token. Ensure that the authentication credentials are correct."
            )
        
        now = datetime.now()
        time_formatter = TimeFormatter(now)
        
        headers = {
        "host": "sellingpartnerapi-na.amazon.com",
        "x-amz-access-token": self.access_token,
        "x-amz-date": time_formatter.amazon_auth_format,
        "user-agent": f"{self.client_id}/1 (Python)",
        "Content-Type": "application/json",
        }

        return headers
