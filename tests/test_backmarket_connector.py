from unittest.mock import MagicMock
from JegBridge.connectors.backmarket_connector import BackmarketConnector


def make_connector():
    """Helper to create a BackmarketConnector with a mock auth object."""
    mock_auth = MagicMock()
    return BackmarketConnector(auth=mock_auth), mock_auth


# --- get_orders ---

def test_get_orders_returns_list():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {
        "results": [{"order_id": 111}, {"order_id": 222}]
    }
    orders = connector.get_orders()
    assert isinstance(orders, list)


def test_get_orders_returns_correct_orders():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {
        "results": [{"order_id": 111}, {"order_id": 222}]
    }
    orders = connector.get_orders()
    assert len(orders) == 2
    assert orders[0]["order_id"] == 111


def test_get_orders_raises_on_bad_response():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"error": "Unauthorized"}
    try:
        connector.get_orders()
        assert False, "Expected KeyError"
    except KeyError:
        pass


def test_get_orders_calls_correct_endpoint():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"results": []}
    connector.get_orders()
    call_kwargs = mock_auth.make_request.call_args
    assert "ws/orders" in call_kwargs[1]["endpoint"]


# --- get_order ---

def test_get_order_calls_correct_endpoint():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"order_id": 9183997}
    connector.get_order("9183997")
    call_kwargs = mock_auth.make_request.call_args
    assert "9183997" in call_kwargs[1]["endpoint"]


def test_get_order_returns_dict():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"order_id": 9183997}
    order = connector.get_order("9183997")
    assert isinstance(order, dict)
    assert order.get("order_id") == 9183997


# --- search_returns ---

def test_search_returns_raises_not_implemented():
    connector, _ = make_connector()
    try:
        connector.search_returns(filter_params={})
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        pass
