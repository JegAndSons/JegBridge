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

