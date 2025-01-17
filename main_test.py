import os
from dotenv import load_dotenv
from JegBridge.auth.amazon_auth import AmazonAuth
from JegBridge.auth.ebay_auth import EbayAuth
from JegBridge.auth.walmartmp_auth import WalmartMPAuth
from JegBridge.connectors.amazon_connector import AmazonConnector
from JegBridge.connectors.ebay_connector import EbayConnector
from JegBridge.connectors.walmartmp_connector import WalmartMPConnector

load_dotenv()

amazon_auth = AmazonAuth(
    client_id=os.getenv("AMAZON_CLIENT_ID"),
    client_secret=os.getenv("AMAZON_CLIENT_SECRET"),
    refresh_token=os.getenv("AMAZON_REFRESH_TOKEN"),
)
ebay_auth = EbayAuth(
    dev_client_id=os.getenv("EBAY_DEV_CLIENT_ID"),
    dev_client_secret=os.getenv("EBAY_DEV_CLIENT_SECRET"),
    dev_refresh_token=os.getenv("EBAY_DEV_REFRESH_TOKEN"),
    prod_client_id=os.getenv("EBAY_PROD_CLIENT_ID"),
    prod_client_secret=os.getenv("EBAY_PROD_CLIENT_SECRET"),
    prod_refresh_token=os.getenv("EBAY_PROD_REFRESH_TOKEN"),
)

ebay_auth.use_production=True

walmartmp_auth = WalmartMPAuth(
        dev_client_id="WALMARTMP_CLIENT_ID",
        dev_client_secret="WALMARTMP_CLIENT_SECRET",
        prod_client_id=os.getenv("WALMARTMP_PROD_CLIENT_ID"),
        prod_client_secret=os.getenv("WALMARTMP_PROD_CLIENT_SECRET"),
    )

walmartmp_auth.use_production=True



amazon_connector = AmazonConnector(auth=amazon_auth)
ebay_connector = EbayConnector(auth=ebay_auth)
walmartmp_connector = WalmartMPConnector(auth=walmartmp_auth)

ebay_order_id = "12-12583-87541"
amazon_order_id = "111-3749347-1157024"
walmartmp_purchase_order_id="109001836611078"

ebay_return_id = "5282832144"
ebay_order_for_return_id = "08-12570-61105"

# response = ebay_connector.search_returns(order_id=ebay_order_for_return_id)
# response = ebay_connector.get_order(ebay_order_for_return_id)
# response = amazon_connector.get_order(amazon_order_id)
response = walmartmp_connector.get_order(walmartmp_purchase_order_id)
print(response)
# import json
# with open('return2.json', 'w') as json_file:
#     json.dump(response, json_file, indent=4)

