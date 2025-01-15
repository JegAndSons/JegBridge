from JegBridge.auth.amazon_auth import AmazonAuth
from JegBridge.auth.ebay_auth import EbayAuth
from JegBridge.connectors.amazon_connector import AmazonConnector
from JegBridge.connectors.ebay_connector import EbayConnector

class ConnectorFactory:
    """
    Factory for creating marketplace-specific connectors.
    """

    @staticmethod
    def create_amazon_connector() -> "AmazonConnector":
        """
        Create and return an AmazonConnector instance.

        Returns:
            AmazonConnector: A connector configured for Amazon.
        """
        # Initialize authentication
        amazon_auth = AmazonAuth()

        # Create and return the connector
        return AmazonConnector(auth=amazon_auth)

    @staticmethod
    def create_ebay_connector() -> "EbayConnector":
        """
        Create and return an EbayConnector instance.

        Returns:
            EbayConnector: A connector configured for eBay.
        """
        # Initialize authentication
        ebay_auth = EbayAuth()

        # Create and return the connector
        return EbayConnector(auth=ebay_auth)

