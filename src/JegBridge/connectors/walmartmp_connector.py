import requests
from typing import Optional, Dict, Any
from JegBridge.connectors.base_connector import BaseConnector
from JegBridge.auth.base_auth import BaseAuth

#TODO manage access token so don't have to create new one each instance
class WalmartMPConnector(BaseConnector):
    """
    Amazon-specific implementation of the connector.
    """

    def __init__(self, auth: BaseAuth):
        super().__init__(auth)

    def get_orders(self) -> list:
        """
        Get orders from Walmart.
        """
        mock_orders = [
            {'walmart_order_id':1},
            {'walmart_order_id':2},
            {'walmart_order_id':3},
            {'walmart_order_id':4},
        ]
        return mock_orders
    
    def get_order(self, purchase_order_id: str) -> requests.Response:
        """
        Get specific order from Walmart

        Args:
            purchase_order_id(str): the purchase order id to search for

        Returns:
            requests.Response: The response object that Walmart's api returns

        Reference:
            Amazon SP api documentation:
            https://developer.walmart.com/api/us/mp/orders#operation/getAnOrder    
        """
        endpoint = f"v3/orders/{purchase_order_id}"
        response = self.auth.make_request("GET",endpoint=endpoint)
        return response
    
    def search_returns(self, filter_params: Optional[Dict[str,Any]]   ) -> requests.Response:
        """
        Search for Walmart returns using the Walmart Marketplace Returns API.

        Args:
            filter_params (Optional[Dict[str,Any]]): dictionary of filter paramaters to send in request.

        Returns:
            requests.Response: The response object returned by the WalmartMP API.

        Reference:
            Walmart Marketplace Returns API Documentation.
            https://developer.walmart.com/api/us/mp/returns#operation/getReturns
        """
        endpoint = "v3/returns"  # Update this to the correct endpoint if needed

        response = self.auth.make_request("GET", endpoint=endpoint, params=filter_params)
        print(response.url)
        return response

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    from JegBridge.auth.walmartmp_auth import WalmartMPAuth

    load_dotenv()
    auth = WalmartMPAuth(
        dev_client_id="WALMARTMP_CLIENT_ID",
        dev_client_secret="WALMARTMP_CLIENT_SECRET",
        prod_client_id=os.getenv("WALMARTMP_PROD_CLIENT_ID"),
        prod_client_secret=os.getenv("WALMARTMP_PROD_CLIENT_SECRET"),
    )
    auth.use_production = True

    connector = WalmartMPConnector(auth=auth)

    rma_number = "175159954944563825"
    purchase_order_number = "109000580338218"

    filter_params = {"returnOrderId": rma_number}
    rma = connector.search_returns(filter_params=filter_params)
    order = connector.get_order(purchase_order_id=purchase_order_number)
    print(rma.json())
    print(order.json())
