import requests
from typing import Optional, Dict, Any
from JegBridge.connectors.base_connector import BaseConnector
from JegBridge.auth.base_auth import BaseAuth

class EbayConnector(BaseConnector):
    """
    Ebay-specific implementation of the connector.
    """

    def __init__(self, auth: BaseAuth):
        super().__init__(auth)

    def get_orders(self) -> list:
        """
        Get orders from Ebay.
        """
        mock_orders = [
            {'ebay_order_id':1},
            {'ebay_order_id':2},
            {'ebay_order_id':3},
            {'ebay_order_id':4},
        ]
        return mock_orders
    
    def get_order(self, order_id: str) -> requests.Response:
        """
        Get specific order from Ebay

        Args:
            order_id(str): the order id to search for

        Returns:
            requests.Response: The response object that Ebay's api returns

        Reference:
            Amazon SP api documentation:
            https://developer.ebay.com/api-docs/sell/fulfillment/resources/order/methods/getOrder    
        """
        endpoint = f"sell/fulfillment/v1/order/{order_id}"
        response = self.auth.make_request("GET",endpoint=endpoint, get_headers_callback=self.auth.get_headers_with_bearer)
        return response

    def search_returns(self, filter_params: Optional[Dict[str,Any]]   ) -> requests.Response:
        """
        Search for eBay returns using the eBay Post-Order API.

        Args:
            filter_params (Optional[Dict[str,Any]]): dictionary of filter paramaters to send in request.

        Returns:
            requests.Response: The response object returned by the eBay API.
        
        Reference:
            eBay API Documentation: 
            https://developer.ebay.com/Devzone/post-order/post-order_v2_return_search__get.html
        """
        endpoint = "post-order/v2/return/search"

        response = self.auth.make_request("GET", endpoint=endpoint, get_headers_callback=self.auth.get_headers_with_iaf, params=filter_params)
        return response
    
if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    from JegBridge.auth.ebay_auth import EbayAuth

    load_dotenv()
    auth = EbayAuth(
        dev_client_id=os.getenv("EBAY_DEV_CLIENT_ID"),
        dev_client_secret=os.getenv("EBAY_DEV_CLIENT_SECRET"),
        dev_refresh_token=os.getenv("EBAY_DEV_REFRESH_TOKEN"),
        prod_client_id=os.getenv("EBAY_PROD_CLIENT_ID"),
        prod_client_secret=os.getenv("EBAY_PROD_CLIENT_SECRET"),
        prod_refresh_token=os.getenv("EBAY_PROD_REFRESH_TOKEN"),
    )
    auth.use_production = True

    connector = EbayConnector(auth=auth)

    ebay_order_for_return_id = "08-12570-61105"
    ebay_return_id = "5282832144"

    order = connector.get_order(ebay_order_for_return_id)
    ebay_return = connector.search_returns(filter_params={"order_id":ebay_order_for_return_id})
    ebay_return2 = connector.search_returns(filter_params={"return_id":ebay_return_id})

    print(order.json())
    print(ebay_return.json())
    print(ebay_return2.json())
    
    