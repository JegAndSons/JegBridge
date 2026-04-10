from unittest.mock import MagicMock
from JegBridge.connectors.walmartmp_connector import WalmartMPConnector


def make_connector():
    """Helper to create a WalmartMPConnector with a mock auth object."""
    mock_auth = MagicMock()
    return WalmartMPConnector(auth=mock_auth), mock_auth


# --- get_orders ---

def test_get_orders_returns_list():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {
        "list": {"elements": {"order": [{"purchaseOrderId": "111"}, {"purchaseOrderId": "222"}]}}
    }
    orders = connector.get_orders()
    assert isinstance(orders, list)


def test_get_orders_returns_correct_orders():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {
        "list": {"elements": {"order": [{"purchaseOrderId": "111"}, {"purchaseOrderId": "222"}]}}
    }
    orders = connector.get_orders()
    assert len(orders) == 2
    assert orders[0]["purchaseOrderId"] == "111"


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
    mock_auth.make_request.return_value.json.return_value = {
        "list": {"elements": {"order": []}}
    }
    connector.get_orders()
    call_kwargs = mock_auth.make_request.call_args
    assert "v3/orders" in call_kwargs[1]["endpoint"]


# --- get_order ---

def test_get_order_calls_correct_endpoint():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"order": {"purchaseOrderId": "109000580338218"}}
    connector.get_order("109000580338218")
    call_kwargs = mock_auth.make_request.call_args
    assert "109000580338218" in call_kwargs[1]["endpoint"]


def test_get_order_returns_dict():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"order": {"purchaseOrderId": "109000580338218"}}
    order = connector.get_order("109000580338218")
    assert isinstance(order, dict)
    assert order.get("purchaseOrderId") == "109000580338218"


def test_get_order_raises_on_bad_response():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"error": "Unauthorized"}
    try:
        connector.get_order("109000580338218")
        assert False, "Expected KeyError"
    except KeyError:
        pass


# --- search_returns ---

def test_search_returns_calls_correct_endpoint():
    connector, mock_auth = make_connector()
    connector.search_returns(filter_params={"returnOrderId": "175159954944563825"})
    call_kwargs = mock_auth.make_request.call_args
    assert "v3/returns" in call_kwargs[1]["endpoint"]


def test_search_returns_passes_filter_params():
    connector, mock_auth = make_connector()
    filter_params = {"returnOrderId": "175159954944563825"}
    connector.search_returns(filter_params=filter_params)
    call_kwargs = mock_auth.make_request.call_args
    assert call_kwargs[1]["params"] == filter_params


def test_search_returns_returns_response():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"returnOrders": []}
    response = connector.search_returns(filter_params={})
    assert response is not None
