import requests
from typing import Optional, Dict, Any
from JegBridge.connectors.base_connector import BaseConnector
from JegBridge.auth.base_auth import BaseAuth

class AmazonConnector(BaseConnector):
    """
    Amazon-specific implementation of the connector.
    """

    def __init__(self, auth: BaseAuth):
        super().__init__(auth)

    def get_orders(self) -> list:
        """
        Get orders from Amazon.
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

        Args:
            order_id(str): the order id to search for

        Returns:
            requests.Response: The response object that Amazon's api returns

        Reference:
            Amazon SP api documentation:
            https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#getorder    
        """
        endpoint = f"/orders/v0/orders/{order_id}"
        response = self.auth.make_request("GET",endpoint=endpoint)
        return response
    
    def search_returns(self, filter_params: Optional[Dict[str,Any]]   ) -> requests.Response:
        """
        Search for returns for a given marketplace with a given list of params

        Args:
            filter_params (Optional[Dict[str,Any]]): dictionary of filter paramaters to send in request.

        Returns:
            list: list of return objects
        """
        raise NotImplementedError("Amazon API does not support searching for returns")

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