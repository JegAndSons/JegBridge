
from JegBridge.services.base_service import BaseService
from JegBridge.connectors.base_connector import BaseConnector

class EbayService(BaseService):

    def __init__(self, connector: BaseConnector):
        super().__init__(connector)

    def get_order(self, order_id):
        response = self.connector.get_order(order_id)
        return response.json()
    def get_orders(self):
        raise NotImplementedError
    def get_return(self):
        raise not NotImplementedError
    

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from JegBridge.connectors.ebay_connector import EbayConnector
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
    service = EbayService(connector=connector)

    ebay_order_for_return_id = "08-12570-61105"
    order = service.get_order(ebay_order_for_return_id)

    print(order)