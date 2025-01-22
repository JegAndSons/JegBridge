from abc import ABC, abstractmethod
from JegBridge.auth.base_auth import BaseAuth

class BaseConnector(ABC):
    """
    Abstract base class for marketplace connectors.
    """

    def __init__(self,auth: BaseAuth):
        self.auth = auth

    @abstractmethod
    def fetch_orders(self) -> list:
        """
        Fetch orders from the marketplace.

        Returns:
            list: A list of orders as returned by the marketplace API.
        """
        pass

    @abstractmethod
    def get_order(self,order_id: str) -> dict:
        """
        Get specific order from marketplace

        Args:
            order_id (str): The order id to search for

        Returns:
         dict: The markteplaces order object
        """
        pass
    
    @abstractmethod
    def search_returns(self, *args, **kwargs):
        """
        Search for returns for a given marketplace with a given list of params

        Returns:
            list: list of return objects
        """
        pass

