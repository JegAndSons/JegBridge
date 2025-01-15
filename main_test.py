from JegBridge.factories.connector_factory import ConnectorFactory


amazon_connector = ConnectorFactory.create_amazon_connector()
ebay_connector = ConnectorFactory.create_ebay_connector()

print(amazon_connector.fetch_orders())
print(ebay_connector.fetch_orders())