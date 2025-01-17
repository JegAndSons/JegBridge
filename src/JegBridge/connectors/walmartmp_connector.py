from JegBridge.connectors.base_connector import BaseConnector
from JegBridge.auth.base_auth import BaseAuth

class WalmartMPConnector(BaseConnector):
    """
    Amazon-specific implementation of the connector.
    """

    def __init__(self, auth: BaseAuth):
        super().__init__(auth)

    def fetch_orders(self) -> list:
        """
        Fetch orders from Walmart.
        """
        mock_orders = [
            {'walmart_order_id':1},
            {'walmart_order_id':2},
            {'walmart_order_id':3},
            {'walmart_order_id':4},
        ]
        return mock_orders
    
    def get_order(self, purchase_order_id: str) -> dict:
        """
        Get specific order from Walmart
        """
        endpoint = f"v3/orders/{purchase_order_id}"
        response = self.auth.make_request("GET",endpoint=endpoint)
        return response.json()
