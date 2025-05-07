from typing import Optional
from JegBridge.auth.base_auth import BaseAuth
from JegBridge.utils.custom_exceptions import AuthenticationError
from JegBridge.utils.base64_utils import encode_base64

class BackmarketAuth(BaseAuth):
    """
    Backmarket-specific authentication using OAuth2.
    """

    def __init__(
        self,
        dev_client_id: str = None,
        dev_client_secret: str = None,
        prod_client_id: str = None,
        prod_client_secret: str = None,
        use_production: bool = False,
        sandbox_url: str = None,
        production_url: str = None,
    ):
        """
        Initialize the BackmarketAuth object.

        Args:
            client_id (str): Backmarket client ID.
            client_secret (str): Backmarket client secret.
            refresh_token (str): Refresh token for OAuth2.
            use_production (bool): Whether to use the production environment.
            sandbox_url (str): Optional custom sandbox URL.
            production_url (str): Optional custom production URL.
        """
        # Set marketplace-specific default URLs
        sandbox_url = sandbox_url or "https://preprod.backmarket.com/"
        production_url = production_url or "https://www.backmarket.com/"

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
        """
        Formats and sets self.access_token
        """
        auth_str = f"{self.client_secret}"
        # encoded_auth_string = encode_base64(auth_str)
        self.access_token = f"Basic {auth_str}"


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
        "Authorization":self.access_token,
        "Accept": "application/json",
    }

        return headers
    

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    load_dotenv(

    )
    auth = BackmarketAuth(
        dev_client_id=os.getenv("BACKMARKET_DEV_CLIENT_ID"),
        dev_client_secret=os.getenv("BACKMARKET_DEV_CLIENT_SECRET"),
        prod_client_id=os.getenv("BACKMARKET_ID"),
        prod_client_secret=os.getenv("BACKMARKET_TOKEN"),
    )
    auth.use_production = True
    auth.authenticate()
    print(auth.base_url)

    headers = auth.get_headers()
    print(headers)

    order_id = "9183997"
    endpoint = f"ws/orders/{order_id}"

    response = auth.make_request("GET",endpoint)
    print(response.content)
    print(response.status_code)
    print(response.json())


    
