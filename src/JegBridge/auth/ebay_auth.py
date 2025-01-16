import requests
import base64
from typing import Optional
from JegBridge.auth.base_auth import BaseAuth

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
        encoded_oath_string = base64.b64encode(oath_string.encode('utf-8')).decode('utf-8')
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
        self.authenticate()
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",  # Required for JSON payloads
        }
        return headers