from unittest.mock import MagicMock
from JegBridge.connectors.ebay_connector import EbayConnector


def make_connector():
    """Helper to create an EbayConnector with a mock auth object."""
    mock_auth = MagicMock()
    return EbayConnector(auth=mock_auth), mock_auth


# --- get_orders ---

def test_get_orders_returns_list():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {
        "orders": [{"orderId": "08-111"}, {"orderId": "08-222"}]
    }
    orders = connector.get_orders()
    assert isinstance(orders, list)


def test_get_orders_returns_correct_orders():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {
        "orders": [{"orderId": "08-111"}, {"orderId": "08-222"}]
    }
    orders = connector.get_orders()
    assert len(orders) == 2
    assert orders[0]["orderId"] == "08-111"


def test_get_orders_returns_empty_list_when_no_orders():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {}
    orders = connector.get_orders()
    assert orders == []


def test_get_orders_calls_correct_endpoint():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"orders": []}
    connector.get_orders()
    call_kwargs = mock_auth.make_request.call_args
    assert call_kwargs[1]["endpoint"] == "sell/fulfillment/v1/order"


def test_get_orders_uses_bearer_headers():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"orders": []}
    connector.get_orders()
    call_kwargs = mock_auth.make_request.call_args
    assert call_kwargs[1]["get_headers_callback"] == mock_auth.get_headers_with_bearer


# --- get_order ---

def test_get_order_calls_correct_endpoint():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"orderId": "08-12570-61105"}
    connector.get_order("08-12570-61105")
    call_kwargs = mock_auth.make_request.call_args
    assert "08-12570-61105" in call_kwargs[1]["endpoint"]


def test_get_order_uses_bearer_headers():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"orderId": "08-12570-61105"}
    connector.get_order("08-12570-61105")
    call_kwargs = mock_auth.make_request.call_args
    assert call_kwargs[1]["get_headers_callback"] == mock_auth.get_headers_with_bearer


def test_get_order_returns_dict():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"orderId": "08-12570-61105"}
    order = connector.get_order("08-12570-61105")
    assert isinstance(order, dict)
    assert order.get("orderId") == "08-12570-61105"


# --- search_returns ---

def test_search_returns_calls_correct_endpoint():
    connector, mock_auth = make_connector()
    connector.search_returns(filter_params={"order_id": "08-12570-61105"})
    call_kwargs = mock_auth.make_request.call_args
    assert "post-order/v2/return/search" in call_kwargs[1]["endpoint"]


def test_search_returns_passes_filter_params():
    connector, mock_auth = make_connector()
    filter_params = {"order_id": "08-12570-61105"}
    connector.search_returns(filter_params=filter_params)
    call_kwargs = mock_auth.make_request.call_args
    assert call_kwargs[1]["params"] == filter_params


def test_search_returns_uses_iaf_headers():
    connector, mock_auth = make_connector()
    connector.search_returns(filter_params={})
    call_kwargs = mock_auth.make_request.call_args
    assert call_kwargs[1]["get_headers_callback"] == mock_auth.get_headers_with_iaf


def test_search_returns_returns_response():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"returns": []}
    response = connector.search_returns(filter_params={})
    assert response is not None
