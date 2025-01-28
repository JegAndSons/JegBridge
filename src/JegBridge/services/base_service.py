from abc import ABC, abstractmethod
from JegBridge.connectors.base_connector import BaseConnector


class BaseService(ABC):

    def __init__(self, connector: BaseConnector):
        self.connector = connector

    @abstractmethod
    def get_order(self, order_id):
        pass
    @abstractmethod 
    def get_orders(self):
        pass
    @abstractmethod
    def get_return(self):
        pass