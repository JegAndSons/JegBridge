"""
Amazon Live Integration Tests
------------------------------
These tests hit the real Amazon SP-API. They are NOT part of the standard test suite.
Run manually to verify credentials and connectivity:

    python tests/amazon_live_test.py

Requirements:
    - A .env file in the project root with the following keys:
        AMAZON_CLIENT_ID
        AMAZON_CLIENT_SECRET
        AMAZON_REFRESH_TOKEN
"""

import os
from dotenv import load_dotenv
from JegBridge.auth.amazon_auth import AmazonAuth
from JegBridge.connectors.amazon_connector import AmazonConnector

load_dotenv()


def make_connector() -> AmazonConnector:
    auth = AmazonAuth(
        client_id=os.getenv("AMAZON_CLIENT_ID"),
        client_secret=os.getenv("AMAZON_CLIENT_SECRET"),
        refresh_token=os.getenv("AMAZON_REFRESH_TOKEN"),
        use_production=True,
    )
    return AmazonConnector(auth=auth, seller_id=os.getenv("AMAZON_SELLER_ID"))


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
    print(f"Unshipped orders retrieved (last 7 days): {len(orders)}")
    if orders:
        print(f"First order ID: {orders[0].get('AmazonOrderId')}")
    print("PASSED")


def test_get_order():
    print("\n--- test_get_order ---")
    connector = make_connector()
    orders = connector.get_orders()
    if not orders:
        print("SKIPPED — no orders available to test get_order")
        return
    order_id = orders[0].get("AmazonOrderId")
    order = connector.get_order(order_id)
    assert isinstance(order, dict), f"Expected dict, got {type(order)}"
    assert order.get("AmazonOrderId") == order_id, "Order ID mismatch"
    print(f"Order retrieved: {order.get('AmazonOrderId')}")
    print("PASSED")


def test_get_listing():
    print("\n--- test_get_listing ---")
    sku = input("Enter a SKU to test get_listing (or press Enter to skip): ").strip()
    if not sku:
        print("SKIPPED")
        return
    connector = make_connector()
    response = connector.get_listing(sku)
    data = response.json()
    print(f"Listing response keys: {list(data.keys())}")
    print("PASSED")


if __name__ == "__main__":
    print("Running Amazon live integration tests...")
    test_authentication()
    test_get_orders()
    test_get_order()
    test_get_listing()
    print("\nAll live tests completed.")
