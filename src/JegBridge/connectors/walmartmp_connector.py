import requests
from typing import Optional
from JegBridge.connectors.base_connector import BaseConnector
from JegBridge.auth.base_auth import BaseAuth

#TODO manage access token so don't have to create new one each instance
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
    
    def get_order(self, purchase_order_id: str) -> requests.Response:
        """
        Get specific order from Walmart
        """
        endpoint = f"v3/orders/{purchase_order_id}"
        response = self.auth.make_request("GET",endpoint=endpoint)
        return response
    
    def search_returns(
    self,
        return_order_id: Optional[str] = None,
        customer_order_id: Optional[str] = None,
        status: Optional[str] = None,
        replacement_info: Optional[bool] = None,
        return_type: Optional[str] = None,
        return_creation_start_date: Optional[str] = None,
        return_creation_end_date: Optional[str] = None,
        return_last_modified_start_date: Optional[str] = None,
        return_last_modified_end_date: Optional[str] = None,
        limit: Optional[int] = 10,
    ) -> requests.Response:
        """
        Search for Walmart returns using the Walmart Marketplace Returns API.

        Args:
            return_order_id (Optional[str]): Return order identifier (RMA number).
            customer_order_id (Optional[str]): Unique ID associated with the sales order for the customer.
            status (Optional[str]): Status of the return order (e.g., INITIATED, DELIVERED, COMPLETED).
            replacement_info (Optional[bool]): Additional attributes related to replacement return order.
            return_type (Optional[str]): Type of the return (e.g., PREORDER, REPLACEMENT, REFUND).
            return_creation_start_date (Optional[str]): Start date for querying created return orders (ISO 8601).
            return_creation_end_date (Optional[str]): End date for querying created return orders (ISO 8601).
            return_last_modified_start_date (Optional[str]): Start date for querying modified return orders (ISO 8601).
            return_last_modified_end_date (Optional[str]): End date for querying modified return orders (ISO 8601).
            limit (Optional[int]): The number of return orders to be returned (default: 10, max: 200).

        Returns:
            requests.Response: The response object returned by the WalmartMP API.

        Reference:
            Walmart Marketplace Returns API Documentation.
        """
        endpoint = "v3/returns"  # Update this to the correct endpoint if needed
        params = {
            "returnOrderId": return_order_id,
            "customerOrderId": customer_order_id,
            "status": status,
            "replacementInfo": str(replacement_info).lower() if replacement_info is not None else None,
            "returnType": return_type,
            "returnCreationStartDate": return_creation_start_date,
            "returnCreationEndDate": return_creation_end_date,
            "returnLastModifiedStartDate": return_last_modified_start_date,
            "returnLastModifiedEndDate": return_last_modified_end_date,
            "limit": limit,
        }

        # Remove None values from params
        params = {key: value for key, value in params.items() if value is not None}
        print(params)

        response = self.auth.make_request("GET", endpoint=endpoint, params=params)
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

    rma = connector.search_returns(return_order_id=rma_number)
    order = connector.get_order(purchase_order_id=purchase_order_number)
    print(rma.json())
    print(order.json())
