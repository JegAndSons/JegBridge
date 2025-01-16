from JegBridge.connectors.base_connector import BaseConnector
from JegBridge.auth.base_auth import BaseAuth

class EbayConnector(BaseConnector):
    """
    Ebay-specific implementation of the connector.
    """

    def __init__(self, auth: BaseAuth):
        super().__init__(auth)

    def fetch_orders(self) -> list:
        """
        Fetch orders from Ebay.
        """
        mock_orders = [
            {'ebay_order_id':1},
            {'ebay_order_id':2},
            {'ebay_order_id':3},
            {'ebay_order_id':4},
        ]
        return mock_orders
    
    def get_order(self, order_id: str) -> dict:
        endpoint = f"sell/fulfillment/v1/order/{order_id}"
        response = self.auth.make_request("GET",endpoint=endpoint, get_headers_callback=self.auth.get_headers_with_bearer)
        response.raise_for_status()
        return response.json()

    def get_return(self, order_id: str) -> dict:
        endpoint = f"post-order/v2/return/search"
        params = {
            "order_id": order_id
        }
        response = self.auth.make_request("GET",endpoint=endpoint,  params=params, get_headers_callback=self.auth.get_headers_with_iaf)
        response.raise_for_status()
        return response.json()
