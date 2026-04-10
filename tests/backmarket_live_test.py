"""
Backmarket Live Integration Tests
-----------------------------------
These tests hit the real Backmarket API. They are NOT part of the standard test suite.
Run manually to verify credentials and connectivity:

    python tests/backmarket_live_test.py

Requirements:
    - A .env file in the project root with the following keys:
        BACKMARKET_ID
        BACKMARKET_TOKEN
"""

import os
from dotenv import load_dotenv
from JegBridge.auth.backmarket_auth import BackmarketAuth
from JegBridge.connectors.backmarket_connector import BackmarketConnector

load_dotenv()


def make_connector() -> BackmarketConnector:
    auth = BackmarketAuth(
        dev_client_id=os.getenv("BACKMARKET_DEV_CLIENT_ID"),
        dev_client_secret=os.getenv("BACKMARKET_DEV_CLIENT_SECRET"),
        prod_client_id=os.getenv("BACKMARKET_ID"),
        prod_client_secret=os.getenv("BACKMARKET_TOKEN"),
    )
    auth.use_production = True
    return BackmarketConnector(auth=auth)


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
        print(f"First order ID: {orders[0].get('order_id')}")
    print("PASSED")


def test_get_order():
    print("\n--- test_get_order ---")
    connector = make_connector()
    orders = connector.get_orders()
    if not orders:
        print("SKIPPED — no orders available to test get_order")
        return
    order_id = str(orders[0].get("order_id"))
    response = connector.get_order(order_id)
    assert response.ok, f"Request failed with status {response.status_code}: {response.text}"
    data = response.json()
    print(f"Order retrieved: {data.get('order_id')}")
    print("PASSED")


if __name__ == "__main__":
    print("Running Backmarket live integration tests...")
    test_authentication()
    test_get_orders()
    test_get_order()
    print("\nAll live tests completed.")
