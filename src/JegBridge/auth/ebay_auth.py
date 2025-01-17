import requests
from typing import Optional, Callable, Dict
from JegBridge.auth.base_auth import BaseAuth
from JegBridge.utils.custom_exceptions import AuthenticationError
from JegBridge.utils.base64_utils import encode_base64

# TODO WHEN RESOLVED: Fix refresh token functionality so only gets new token when needed. Deal with access token errors such as invalid or like how it is in sandbox since ebay's sandbox is broken

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

    @property
    def client_id(self) -> str:
        return self._prod_client_id if self.use_production else self._dev_client_id

    @property
    def client_secret(self) -> str:
        return self._prod_client_secret if self.use_production else self._dev_client_secret

    @property
    def refresh_token(self) -> str:
        return self._prod_refresh_token if self.use_production else self._dev_refresh_token

    def authenticate(self):
        refresh_url = f"{self.base_url}identity/v1/oauth2/token"

        oath_string = f"{self.client_id}:{self.client_secret}"
        encoded_oath_string = encode_base64(oath_string)
        password = f"Basic {encoded_oath_string}"

        headers = {
            "Content-Type":"application/x-www-form-urlencoded",
            "Authorization":password
        }

        body = {
            "grant_type":"refresh_token",
            "refresh_token":self.refresh_token,
        }

        response = requests.post(refresh_url,headers=headers,data=body)

        response_json = response.json()

        self.access_token = response_json['access_token']

    def get_headers(self):
        raise NotImplementedError
    
    def get_headers_with_bearer(self):
        """
        Get headers that pass bearer token, like for fulfillment api
        """
        self.authenticate()
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
        self.authenticate()
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