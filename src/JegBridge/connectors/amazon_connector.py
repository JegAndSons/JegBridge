from JegBridge.connectors.base_connector import BaseConnector
from JegBridge.auth.base_auth import BaseAuth

class AmazonConnector(BaseConnector):
    """
    Amazon-specific implementation of the connector.
    """

    def __init__(self, auth: BaseAuth):
        super().__init__(auth)

    def fetch_orders(self) -> list:
        """
        Fetch orders from Amazon.
        """
        mock_orders = [
            {'amazon_order_id':1},
            {'amazon_order_id':2},
            {'amazon_order_id':3},
            {'amazon_order_id':4},
        ]
        return mock_orders
