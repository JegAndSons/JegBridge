import uuid
import requests
from typing import Optional
from JegBridge.auth.base_auth import BaseAuth
from JegBridge.utils.custom_exceptions import AuthenticationError
from JegBridge.utils.base64_utils import encode_base64

class WalmartMPAuth(BaseAuth):
    """
    WalmartMP-specific authentication using OAuth2.
    """

    def __init__(
        self,
        dev_client_id: str,
        dev_client_secret: str,
        prod_client_id: str = None,
        prod_client_secret: str = None,
        use_production: bool = False,
        sandbox_url: str = None,
        production_url: str = None,
    ):
        """
        Initialize the AmazonAuth object.

        Args:
            client_id (str): Walamrt client ID.
            client_secret (str): Walamrt client secret.
            refresh_token (str): Refresh token for OAuth2.
            use_production (bool): Whether to use the production environment.
            sandbox_url (str): Optional custom sandbox URL.
            production_url (str): Optional custom production URL.
        """
        # Set marketplace-specific default URLs
        sandbox_url = sandbox_url or "https://sandbox.walmartapis.com/"
        production_url = production_url or "https://marketplace.walmartapis.com/"

        super().__init__(use_production, sandbox_url, production_url)

        self._dev_client_id = dev_client_id
        self._dev_client_secret = dev_client_secret
        self._prod_client_id = prod_client_id
        self._prod_client_secret = prod_client_secret
        self.access_token: Optional[str] = None

    @property
    def client_id(self) -> str:
        return self._prod_client_id if self.use_production else self._dev_client_id

    @property
    def client_secret(self) -> str:
        return self._prod_client_secret if self.use_production else self._dev_client_secret

    def authenticate(self):
        auth_str = f"{self.client_id}:{self.client_secret}"
        encoded_oath_string = encode_base64(auth_str)
        endpoint = "v3/token"
        token_url = self.base_url + endpoint

        headers = {
            "Authorization":f"Basic {encoded_oath_string}",
            "Accept":"application/json",
            "WM_SVC.NAME":"Walmart Marketplace",
            "WM_QOS.CORRELATION_ID":self.generate_guid(),
        }
        data = {
            "grant_type":"client_credentials"
        }

        response = requests.post(token_url, headers=headers, data=data)

        self.access_token = response.json().get('access_token')
        response.raise_for_status()


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
        
        
        headers = {
        "WM_SEC.ACCESS_TOKEN":self.access_token,
        "WM_QOS.CORRELATION_ID":self.generate_guid(),
        "WM_SVC.NAME":"Walmart Marketplace",
        "Accept": "application/json",
    }

        return headers
    
    def generate_guid(self) -> str:
        return str(uuid.uuid4())


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    load_dotenv(

    )
    auth = WalmartMPAuth(
        dev_client_id="WALMARTMP_CLIENT_ID",
        dev_client_secret="WALMARTMP_CLIENT_SECRET",
        prod_client_id=os.getenv("WALMARTMP_PROD_CLIENT_ID"),
        prod_client_secret=os.getenv("WALMARTMP_PROD_CLIENT_SECRET"),
    )
    auth.use_production = True
    auth.authenticate()

    headers = {
        "WM_SEC.ACCESS_TOKEN":auth.access_token,
        "WM_QOS.CORRELATION_ID":auth.generate_guid(),
        "WM_SVC.NAME":"Walmart Marketplace",
        "Accept": "application/json",
    }

    purchase_order_id = "109001836611078"
    endpoint = f"v3/orders/{purchase_order_id}"
    
    response = auth.make_request("GET",endpoint=endpoint)
    print(response.json())
    print(response.status_code)
