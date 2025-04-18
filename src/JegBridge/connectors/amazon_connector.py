import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from JegBridge.connectors.base_connector import BaseConnector
from JegBridge.auth.base_auth import BaseAuth
# from JegBridge.mixins.amazon_report_handler import AmazonReportHandler

class AmazonConnector(BaseConnector):
    """
    Amazon-specific implementation of the connector.
    """

    SELLER_ID = "A3NSC2CS6ZUMAC"

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
    
    def create_report(
        self, 
        report_type: str, 
        marketplaces: List[str] = None, 
        data_start_date: Optional[datetime] = None, 
        data_end_date: Optional[datetime] = None, 
        report_options: Optional[Dict] = None
    ):
        """
        Create an Amazon report request.

        Args:
            report_type (str): The type of report to generate.
            marketplaces (List[str], optional): List of marketplace IDs. Defaults to ["ATVPDKIKX0DER"].
            data_start_time (datetime, optional): Start time for report data (ISO 8601).
            data_end_date (datetime, optional): End time for report data (ISO 8601).
            report_options (Dict, optional): Additional report options.

        returns:
            requests.Response: The response object returned by the api containing the report id.

        Reference:
            https://developer-docs.amazon.com/sp-api/docs/reports-api-v2021-06-30-reference#post-reports2021-06-30reports
        """
        endpoint = "reports/2021-06-30/reports"

        # Ensure marketplaces is a list, defaulting to ["ATVPDKIKX0DER"]
        marketplaces = marketplaces or ["ATVPDKIKX0DER"]

        # Ensure report_options is always included in the request, defaulting to an empty dictionary
        report_options = report_options or {}

        # Build request payload
        data = {
            "reportType": report_type,
            "marketplaceIds": marketplaces,
            "dataStartTime": data_start_date.isoformat() if data_start_date else None,
            "dataEndTime": data_end_date.isoformat() if data_end_date else None,
            "reportOptions": report_options
        }

        # Remove None values to avoid sending unnecessary null fields
        data = {key: value for key, value in data.items() if value is not None}

        # Make the API request
        response = self.auth.make_request("POST", endpoint, data=json.dumps(data))

        return response
    
    def get_report_info(self,report_id):
        endpoint = f"reports/2021-06-30/reports/{report_id}"
        response = self.auth.make_request("GET", endpoint)
        
        return response
    
    def get_doc_url(self,doc_id):
        endpoint = f"reports/2021-06-30/documents/{doc_id}"
        response = self.auth.make_request("GET", endpoint)

        return response
    
    def get_listing(self, sku):
        endpoint = f"/listings/2021-08-01/items/{self.SELLER_ID}/{sku}"
        params = {
            "marketplaceIds":"ATVPDKIKX0DER",
            "issueLocale":"en_US",
            "includedData":"fulfillmentAvailability,attributes, summaries"
        }
        response = self.auth.make_request("GET",endpoint=endpoint, params=params)
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
