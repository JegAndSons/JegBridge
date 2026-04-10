import requests
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
from JegBridge.connectors.base_connector import BaseConnector
from JegBridge.auth.base_auth import BaseAuth
from JegBridge.mixins.amazon_report_handler import AmazonReportHandler
from JegBridge.mixins.amazon_listing_handler import AmazonListingHandler

class AmazonConnector(BaseConnector, AmazonReportHandler, AmazonListingHandler):
    """
    Amazon-specific implementation of the connector.
    """

    def __init__(self, auth: BaseAuth, seller_id: str):
        super().__init__(auth)
        self.seller_id = seller_id


    def get_orders(self) -> list:
        """
        Get unshipped orders from Amazon created in the last 7 days.

        Returns:
            list: A list of order objects as returned by the Amazon SP-API.

        Raises:
            KeyError: If the response structure is unexpected.

        Reference:
            https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#getorders
        """
        params = {
            "MarketplaceIds": ["ATVPDKIKX0DER", "A2EUQ1WTGCTBG2"],
            "CreatedAfter": (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "OrderStatuses": "Unshipped",
        }

        response = self.auth.make_request("GET", endpoint="orders/v0/orders", params=params)
        data = response.json()

        if "payload" not in data or "Orders" not in data["payload"]:
            raise KeyError(f"Unexpected response structure from Amazon orders API: {data}")

        return data["payload"]["Orders"]
    
    def get_order(self, order_id: str) -> dict:
        """
        Get specific order from Amazon.

        Args:
            order_id(str): the order id to search for

        Returns:
            dict: The order object.

        Raises:
            KeyError: If the response structure is unexpected.

        Reference:
            https://developer-docs.amazon.com/sp-api/docs/orders-api-v0-reference#getorder
        """
        endpoint = f"/orders/v0/orders/{order_id}"
        response = self.auth.make_request("GET", endpoint=endpoint)
        data = response.json()

        if "payload" not in data:
            raise KeyError(f"Unexpected response structure from Amazon get_order API: {data}")

        return data["payload"]
    
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
    import csv
    import io
    from dotenv import load_dotenv
    from JegBridge.auth.amazon_auth import AmazonAuth

    load_dotenv()

    auth = AmazonAuth(
        client_id=os.getenv("AMAZON_CLIENT_ID"),
        client_secret=os.getenv("AMAZON_CLIENT_SECRET"),
        refresh_token=os.getenv("AMAZON_REFRESH_TOKEN"),
        )
    
    connector = AmazonConnector(auth=auth)

    # order_id = "111-3749347-1157024"

    # order = connector.get_order(order_id)
    # print(order.json())
    # orders = connector.get_orders()
    # print(len(orders))



    print("trying to create report..........................................................")
    # create_report_response = connector.create_report(
    #     report_type="GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE",
    #     marketplaces=["ATVPDKIKX0DER"],
    #     data_start_date=datetime.now(timezone.utc) - timedelta(days=30),
    #     data_end_date=None,
    #     report_options={}
    # )
    # print(create_report_response.json())
    # report_id = create_report_response.json()["reportId"]
    
    report_id = "1708293020229"
    report_info = connector.get_report_info(report_id)
    report_info_json = report_info.json()
    # print(report_info_json)

    # Extract the document ID from the report info
    report_document_id = report_info_json.get("reportDocumentId")
    print(f"report_document_id: {report_document_id}")

    if report_document_id:
        doc_response = connector.get_doc_url(report_document_id)
        doc_info = doc_response.json()
        print(f"doc_info: {doc_info}")

        presigned_url = doc_info.get("url")
        # print(f"presigned_url: {presigned_url}")

        if presigned_url:
            report_response = requests.get(presigned_url)
            if report_response.status_code == 200:
                report_data_bytes = report_response.content
                # print(f"report_data: {report_data[:500]}")
                print(type(report_data_bytes))
                report_data_str = report_data_bytes.decode("iso-8859-1")
                print(type(report_data_str))
                report_data_str_io = io.StringIO(report_data_str)
                report_data_csv = csv.reader(report_data_str_io, delimiter="\t")
                for row in report_data_csv:
                    print(row)


            else:
                print(f"Failed to download report. Status code: {report_response.status_code}")


#testing getting listings

# from JegBridge.auth.amazon_auth import AmazonAuth
# import os
# from dotenv import load_dotenv

# load_dotenv()

# auth = AmazonAuth(
#     client_id=os.getenv("AMAZON_CLIENT_ID"),
#     client_secret=os.getenv("AMAZON_CLIENT_SECRET"),
#     refresh_token=os.getenv("AMAZON_REFRESH_TOKEN"),
#     )


# connector = AmazonConnector(auth=auth)

# today_orders = connector.get_orders()
# print(f"today_orders: {today_orders}")