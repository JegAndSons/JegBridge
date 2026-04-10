from typing import Optional, Dict, List, TYPE_CHECKING, Protocol
import json
from datetime import datetime

if TYPE_CHECKING:
    from JegBridge.auth.base_auth import BaseAuth

class HasAuth(Protocol):
    auth: "BaseAuth"

class AmazonReportHandler:
    """
    Amazon-specific implementation of the report handler. auth is expected to be an instance of AmazonAuth, which is a subclass of BaseAuth.
     This mixin provides methods for handling Amazon reports, such as parsing returns data.
    """
    def create_report(
        self: "HasAuth",
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
    
    def get_report_info(self: "HasAuth", report_id):
        endpoint = f"reports/2021-06-30/reports/{report_id}"
        response = self.auth.make_request("GET", endpoint)
        return response

    def get_doc_url(self: "HasAuth", doc_id):
        endpoint = f"reports/2021-06-30/documents/{doc_id}"
        response = self.auth.make_request("GET", endpoint)
        return response


    def parse_returns(self):
        """
        Parse the returns report data.

        Returns:
            list: List of Amazon returns.
        """
        pass