import time
import requests
from typing import Optional, Callable, Dict
from JegBridge.auth.base_auth import BaseAuth
from JegBridge.utils.custom_exceptions import AuthenticationError, TokenMissingError
from JegBridge.utils.base64_utils import encode_base64

class EbayAuth(BaseAuth):
    """
    eBay-specific authentication using API keys.
    """
    def __init__(
        self,
        dev_client_id: str,
        dev_client_secret: str,
        dev_refresh_token: str,
        prod_client_id: str = None,
        prod_client_secret: str = None,
        prod_refresh_token: str = None,
        use_production: bool = False,
        sandbox_url: str = None,
        production_url: str = None,
    ):
        """
        Initialize the EbayAuth object.

        Args:
            _dev_client_id (str): Dev Amazon client ID.
            _dev_client_secret (str): Dev Amazon client secret.
            _dev_refresh_token (str): Dev Refresh token for OAuth2.
            _prod_client_id (str): Prod Amazon client ID.
            _prod_client_secret (str): Prod Amazon client secret.
            _prod_refresh_token (str): Prod Refresh token for OAuth2.
            use_production (bool): Whether to use the production environment.
            sandbox_url (str): Optional custom sandbox URL.
            production_url (str): Optional custom production URL.
        """
        # Set marketplace-specific default URLs
        sandbox_url = sandbox_url or "https://api.sandbox.ebay.com/"
        production_url = production_url or "https://api.ebay.com/"

        super().__init__(use_production, sandbox_url, production_url)

        self._dev_client_id = dev_client_id
        self._dev_client_secret = dev_client_secret
        self._dev_refresh_token = dev_refresh_token
        self._prod_client_id = prod_client_id
        self._prod_client_secret = prod_client_secret
        self._prod_refresh_token = prod_refresh_token
        self.access_token: Optional[str] = None
        self.token_expiry: Optional[float] = None

    @property
    def client_id(self) -> str:
        return self._prod_client_id if self.use_production else self._dev_client_id

    @property
    def client_secret(self) -> str:
        return self._prod_client_secret if self.use_production else self._dev_client_secret

    @property
    def refresh_token(self) -> str:
        return self._prod_refresh_token if self.use_production else self._dev_refresh_token
    
    def _is_token_valid(self) -> bool:
        return (
            self.access_token is not None and
            self.token_expiry is not None and
            time.time() < self.token_expiry - 60  # leave 60s buffer
        )

    def _ensure_token(self) -> None:
        if not self._is_token_valid():
            self.authenticate()

    def authenticate(self):
        """
        Refreshes self.access_token

        Raises:
            AuthenticationError: If the authentication request fails or the response is invalid.
        """
        refresh_url = f"{self.base_url}identity/v1/oauth2/token"

        auth_string = f"{self.client_id}:{self.client_secret}"
        encoded_auth_string = encode_base64(auth_string)
        password = f"Basic {encoded_auth_string}"

        headers = {
            "Content-Type":"application/x-www-form-urlencoded",
            "Authorization":password
        }

        body = {
            "grant_type":"refresh_token",
            "refresh_token":self.refresh_token,
        }

        try:

            response = requests.post(refresh_url,headers=headers,data=body)
            response.raise_for_status()

            data = response.json()

            self.access_token = data.get('access_token')
            expires_in = data.get('expires_in')

            if not self.access_token:
                raise TokenMissingError(
                    "Authentication succeeded but 'access_token' is missing in the response. "
                    "Check the API response format or credentials."
                )
            
            self.token_expiry = time.time() + expires_in if expires_in else None

        except requests.exceptions.RequestException as e:
            raise AuthenticationError(
                f"Failed to authenticate with eBay API. Check your network connection, API URL, "
                f"or credentials. Details: {e}"
            )

        except ValueError as e:
            raise AuthenticationError(
                f"Failed to parse the authentication response as JSON. Ensure the API is returning valid JSON. "
                f"Details: {e}"
            )
        
    
    def get_headers(self):
        raise NotImplementedError
    
    def get_headers_with_bearer(self):
        """
        Get headers that pass bearer token, like for fulfillment api
        """
        self._ensure_token() 

        # Ensure the access token exists before returning headers
        if not self.access_token:
            raise AuthenticationError(
                "Unable to retrieve access token. Ensure that the authentication credentials are correct."
            )
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",  # Required for JSON payloads
        }
        return headers
    
    def get_headers_with_iaf(self):
        """
        Get headers that pass iaf token, like for post-order api
        """
        self._ensure_token() 

        # Ensure the access token exists before returning headers
        if not self.access_token:
            raise AuthenticationError(
                "Unable to retrieve access token. Ensure that the authentication credentials are correct."
            )
        headers = {
            "Authorization": f"IAF {self.access_token}",
            "Content-Type": "application/json",  # Required for JSON payloads
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_US", 
        }
        return headers
    
    def make_request(
        self,
        method: str,
        endpoint: str,
        get_headers_callback: Optional[Callable[[], Dict[str, str]]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make an HTTP request with error handling for NotImplementedError.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            endpoint (str): Endpoint relative to the base URL.
            get_headers_callback: Callable that returns headers dictionary. Defaults to `self.get_headers`.
            **kwargs: Additional arguments to pass to the `requests.request` method.

        Returns:
            requests.Response: The response object.

        Raises:
            RequestError: If the request fails or returns a non-200 status code.
            NotImplementedError: If `self.get_headers` is not overridden and used improperly.
        """
        if get_headers_callback is None:
            get_headers_callback = self.get_headers  # Default to `self.get_headers`

        try:
            # Call the parent class's `make_request` method with the appropriate headers
            return super().make_request(
                method=method,
                endpoint=endpoint,
                get_headers_callback=get_headers_callback,
                **kwargs,
            )
        except NotImplementedError:
            raise NotImplementedError(
                "The default `get_headers` method is not implemented. "
                "Please provide a specific `get_headers_callback`, such as `get_headers_with_bearer` or `get_headers_with_iaf`."
            )