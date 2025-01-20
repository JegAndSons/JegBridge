import requests
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
    
    def get_order(self, order_id: str) -> requests.Response:
        """
        Get specific order from Amazon
        """
        endpoint = f"/orders/v0/orders/{order_id}"
        response = self.auth.make_request("GET",endpoint=endpoint)
        return response

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from JegBridge.auth.amazon_auth import AmazonAuth

    load_dotenv()

    auth = AmazonAuth(
        client_id=os.getenv("AMAZON_CLIENT_ID"),
        client_secret=os.getenv("AMAZON_CLIENT_SECRET"),
        refresh_token=os.getenv("AMAZON_REFRESH_TOKEN"),
        )
    
    connector = AmazonConnector(auth=auth)

    order_id = "111-3749347-1157024"

    order = connector.get_order(order_id)

    print(order.json())