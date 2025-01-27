import requests
from JegBridge.connectors.base_connector import BaseConnector
from JegBridge.auth.base_auth import BaseAuth

#TODO manage access token so don't have to create new one each instance
class BackmarketConnector(BaseConnector):
    """
    Amazon-specific implementation of the connector.
    """

    def __init__(self, auth: BaseAuth):
        super().__init__(auth)

    def get_orders(self) -> list:
        """
        Get orders from Backmarket.
        """
        mock_orders = [
            {'backmarket_order_id':1},
            {'backmarket_order_id':2},
            {'backmarket_order_id':3},
            {'backmarket_order_id':4},
        ]
        return mock_orders
    
    def get_order(self, order_id: str) -> requests.Response:
        """
        Get specific order from Backmarket

        Args:
            order_id(str): the order id to search for

        Returns:
            requests.Response: The response object that Backmarket's api returns

        Reference:
            Amazon SP api documentation:
            https://api.backmarket.dev/#/operations/get-ws-specific-order    
        """
        endpoint = f"ws/orders/{order_id}"
        response = self.auth.make_request("GET",endpoint=endpoint)
        return response
    
    
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from JegBridge.auth.backmarket_auth import BackmarketAuth

    load_dotenv()

    auth = BackmarketAuth(
        dev_client_id=os.getenv("BACKMARKET_DEV_CLIENT_ID"),
        dev_client_secret=os.getenv("BACKMARKET_DEV_CLIENT_SECRET"),
        prod_client_id=os.getenv("BACKMARKET_PROD_CLIENT_ID"),
        prod_client_secret=os.getenv("BACKMARKET_PROD_CLIENT_SECRET"),
    )
    auth.use_production = True

    connector = BackmarketConnector(auth=auth)


    order_id = "9183997"
    order = connector.get_order(order_id)

    print(order.json())