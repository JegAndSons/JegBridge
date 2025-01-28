import requests
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from JegBridge.auth.base_auth import BaseAuth


class BaseConnector(ABC):
    """
    Abstract base class for marketplace connectors.
    """

    def __init__(self, auth: BaseAuth):
        self.auth = auth

    @abstractmethod
    def get_orders(self) -> list:
        """
        Get orders from the marketplace.

        Returns:
            list: A list of orders as returned by the marketplace API.
        """
        pass

    @abstractmethod
    def get_order(self, order_id: str) -> requests.Response:
        """
        Get specific order from marketplace

        Args:
            order_id (str): The order id to search for

        Returns:
         dict: The markteplaces order object
        """
        pass

    @abstractmethod
    def search_returns(self, filter_params: Optional[Dict[str,Any]]   ) -> requests.Response:
        """
        Search for returns for a given marketplace with a given list of params

        Args:
            filter_params (Optional[Dict[str,Any]]): dictionary of filter paramaters to send in request.

        Returns:
            list: list of return objects
        """
        pass
