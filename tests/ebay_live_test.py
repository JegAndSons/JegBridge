"""
eBay Live Integration Tests
----------------------------
These tests hit the real eBay API. They are NOT part of the standard test suite.
Run manually to verify credentials and connectivity:

    python tests/ebay_live_test.py

Requirements:
    - A .env file in the project root with the following keys:
        EBAY_PROD_CLIENT_ID
        EBAY_PROD_CLIENT_SECRET
        EBAY_PROD_REFRESH_TOKEN
"""

import os
from dotenv import load_dotenv
from JegBridge.auth.ebay_auth import EbayAuth
from JegBridge.connectors.ebay_connector import EbayConnector

load_dotenv()


def make_connector() -> EbayConnector:
    auth = EbayAuth(
        dev_client_id=os.getenv("EBAY_DEV_CLIENT_ID"),
        dev_client_secret=os.getenv("EBAY_DEV_CLIENT_SECRET"),
        dev_refresh_token=os.getenv("EBAY_DEV_REFRESH_TOKEN"),
        prod_client_id=os.getenv("EBAY_PROD_CLIENT_ID"),
        prod_client_secret=os.getenv("EBAY_PROD_CLIENT_SECRET"),
        prod_refresh_token=os.getenv("EBAY_PROD_REFRESH_TOKEN"),
    )
    auth.use_production = True
    return EbayConnector(auth=auth)


def test_authentication():
    print("\n--- test_authentication ---")
    auth = make_connector().auth
    auth.authenticate()
    assert auth.access_token is not None, "No access token returned"
    print(f"Access token obtained: {auth.access_token[:20]}...")
    print("PASSED")


def test_get_orders():
    print("\n--- test_get_orders ---")
    connector = make_connector()
    orders = connector.get_orders()
    assert isinstance(orders, list), f"Expected list, got {type(orders)}"
    print(f"Orders retrieved: {len(orders)}")
    if orders:
        print(f"First order ID: {orders[0].get('orderId')}")
    print("PASSED")


def test_get_order():
    print("\n--- test_get_order ---")
    connector = make_connector()
    orders = connector.get_orders()
    if not orders:
        print("SKIPPED — no orders available to test get_order")
        return
    order_id = orders[0].get("orderId")
    order = connector.get_order(order_id)
    assert isinstance(order, dict), f"Expected dict, got {type(order)}"
    assert order.get("orderId") == order_id, "Order ID mismatch"
    print(f"Order retrieved: {order.get('orderId')}")
    print("PASSED")


def test_search_returns():
    print("\n--- test_search_returns ---")
    connector = make_connector()
    response = connector.search_returns(filter_params={"limit": 10})
    data = response.json()
    print(f"Returns response keys: {list(data.keys())}")
    print("PASSED")


if __name__ == "__main__":
    print("Running eBay live integration tests...")
    test_authentication()
    test_get_orders()
    test_get_order()
    test_search_returns()
    print("\nAll live tests completed.")
