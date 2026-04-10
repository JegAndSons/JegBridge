"""
Walmart Marketplace Live Integration Tests
-------------------------------------------
These tests hit the real Walmart MP API. They are NOT part of the standard test suite.
Run manually to verify credentials and connectivity:

    python tests/walmartmp_live_test.py

Requirements:
    - A .env file in the project root with the following keys:
        WALMART_CLIENT_ID
        WALMART_CLIENT_SECRET
"""

import os
from dotenv import load_dotenv
from JegBridge.auth.walmartmp_auth import WalmartMPAuth
from JegBridge.connectors.walmartmp_connector import WalmartMPConnector

load_dotenv()


def make_connector() -> WalmartMPConnector:
    auth = WalmartMPAuth(
        dev_client_id="WALMARTMP_CLIENT_ID",
        dev_client_secret="WALMARTMP_CLIENT_SECRET",
        prod_client_id=os.getenv("WALMART_CLIENT_ID"),
        prod_client_secret=os.getenv("WALMART_CLIENT_SECRET"),
    )
    auth.use_production = True
    return WalmartMPConnector(auth=auth)


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
        print(f"First order ID: {orders[0].get('purchaseOrderId')}")
    print("PASSED")


def test_get_order():
    print("\n--- test_get_order ---")
    connector = make_connector()
    orders = connector.get_orders()
    if not orders:
        print("SKIPPED — no orders available to test get_order")
        return
    order_id = orders[0].get("purchaseOrderId")
    response = connector.get_order(order_id)
    data = response.json()
    assert "order" in data, f"Unexpected response: {data}"
    assert data["order"].get("purchaseOrderId") == order_id, "Order ID mismatch"
    print(f"Order retrieved: {order_id}")
    print("PASSED")


def test_search_returns():
    print("\n--- test_search_returns ---")
    connector = make_connector()
    response = connector.search_returns(filter_params={"limit": 10})
    data = response.json()
    print(f"Returns response keys: {list(data.keys())}")
    print("PASSED")


if __name__ == "__main__":
    print("Running Walmart MP live integration tests...")
    test_authentication()
    test_get_orders()
    test_get_order()
    test_search_returns()
    print("\nAll live tests completed.")
