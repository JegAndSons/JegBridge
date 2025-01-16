from typing import Optional
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

    def search_ebay_returns(
        self,
        creation_date_range_from: Optional[str] = None,
        creation_date_range_to: Optional[str] = None,
        item_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_id: Optional[str] = None,
        return_id: Optional[str] = None,
        return_state: Optional[str] = None,
        role: Optional[str] = None,
        sort: Optional[str] = None,
        states: Optional[str] = None,
        transaction_id: Optional[str] = None
    ) -> dict:
        """
        Search for eBay returns using the eBay Post-Order API.

        Args:
            creation_date_range_from (Optional[str]): The start date for the return creation date range in ISO 8601 format.
            creation_date_range_to (Optional[str]): The end date for the return creation date range in ISO 8601 format.
            item_id (Optional[str]): The unique identifier of the item involved in the return.
            limit (Optional[int]): The maximum number of records to return in the response.
            offset (Optional[int]): The number of records to skip before returning the response.
            order_id (Optional[str]): The unique identifier of the order involved in the return.
            return_id (Optional[str]): The unique identifier of the return request.
            return_state (Optional[str]): Filter to count returns by their state (e.g., OPEN, CLOSED).
            role (Optional[str]): The user role (e.g., BUYER, SELLER) to filter the returns.
            sort (Optional[str]): The field to sort the results (e.g., creation_date).
            states (Optional[str]): The state(s) of the return request (e.g., INITIATED, COMPLETED).
            transaction_id (Optional[str]): The unique identifier of the transaction involved in the return.

        Returns:
            requests.Response: The response object returned by the eBay API.
        
        Reference:
            eBay API Documentation: 
            https://developer.ebay.com/Devzone/post-order/post-order_v2_return_search__get.html
        """
        endpoint = "post-order/v2/return/search"
        params = {
            "creation_date_range_from": creation_date_range_from,
            "creation_date_range_to": creation_date_range_to,
            "item_id": item_id,
            "limit": limit,
            "offset": offset,
            "order_id": order_id,
            "return_id": return_id,
            "return_state": return_state,
            "role": role,
            "sort": sort,
            "states": states,
            "transaction_id": transaction_id
        }

        # Remove None values from params
        params = {key: value for key, value in params.items() if value is not None}

        response = self.auth.make_request("GET", endpoint=endpoint, get_headers_callback=self.auth.get_headers_with_iaf, params=params)
        response.raise_for_status()
        return response.json()
    