class Config:
    def __init__(
            self,
            amazon_client_id: str = None,
            amazon_client_secret: str = None,
            amazon_refresh_token: str = None,
            backmarket_dev_client_id: str = None,
            backmarket_dev_client_secret: str = None,
            backmarket_prod_client_id: str = None,
            backmarket_prod_client_secret: str = None,
            ebay_dev_client_id: str = None,
            ebay_dev_client_secret: str = None,
            ebay_dev_refresh_token: str = None,
            ebay_prod_client_id: str = None,
            ebay_prod_client_secret: str = None,
            ebay_prod_refresh_token: str = None,
            walmartmp_dev_client_id: str = None,
            walmartmp_dev_client_secret: str = None,
            walmartmp_prod_client_id: str = None,
            walmartmp_prod_client_secret: str = None,
    ):
            self.amazon_client_id = amazon_client_id
            self.amazon_client_secret = amazon_client_secret
            self.amazon_refresh_token = amazon_refresh_token
            self.backmarket_dev_client_id = backmarket_dev_client_id
            self.backmarket_dev_client_secret = backmarket_dev_client_secret
            self.backmarket_prod_client_id = backmarket_prod_client_id
            self.backmarket_prod_client_secret = backmarket_prod_client_secret
            self.ebay_dev_client_id = ebay_dev_client_id
            self.ebay_dev_client_secret = ebay_dev_client_secret
            self.ebay_dev_refresh_token = ebay_dev_refresh_token
            self.ebay_prod_client_id = ebay_prod_client_id
            self.ebay_prod_client_secret = ebay_prod_client_secret
            self.ebay_prod_refresh_token = ebay_prod_refresh_token
            self.walmartmp_dev_client_id = walmartmp_dev_client_id
            self.walmartmp_dev_client_secret = walmartmp_dev_client_secret
            self.walmartmp_prod_client_id = walmartmp_prod_client_id
            self.walmartmp_prod_client_secret = walmartmp_prod_client_secret

