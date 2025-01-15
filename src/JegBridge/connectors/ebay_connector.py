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
