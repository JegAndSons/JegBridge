from unittest.mock import MagicMock
from JegBridge.connectors.amazon_connector import AmazonConnector


def make_connector():
    """Helper to create an AmazonConnector with a mock auth object."""
    mock_auth = MagicMock()
    return AmazonConnector(auth=mock_auth, seller_id="TEST_SELLER_ID"), mock_auth


# --- get_orders ---

def test_get_orders_returns_list():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {
        "payload": {"Orders": [{"OrderId": "111"}, {"OrderId": "222"}]}
    }
    orders = connector.get_orders()
    assert isinstance(orders, list)
    assert len(orders) == 2


def test_get_orders_returns_correct_order_ids():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {
        "payload": {"Orders": [{"OrderId": "111-111"}, {"OrderId": "222-222"}]}
    }
    orders = connector.get_orders()
    assert orders[0]["OrderId"] == "111-111"
    assert orders[1]["OrderId"] == "222-222"


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
        "payload": {"Orders": []}
    }
    connector.get_orders()
    call_kwargs = mock_auth.make_request.call_args
    assert call_kwargs[1]["endpoint"] == "orders/v0/orders"


# --- get_order ---

def test_get_order_calls_correct_endpoint():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"payload": {"AmazonOrderId": "111-222-333"}}
    connector.get_order("111-222-333")
    call_kwargs = mock_auth.make_request.call_args
    assert "111-222-333" in call_kwargs[1]["endpoint"]


def test_get_order_returns_dict():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"payload": {"AmazonOrderId": "111-222-333"}}
    order = connector.get_order("111-222-333")
    assert isinstance(order, dict)
    assert order.get("AmazonOrderId") == "111-222-333"


def test_get_order_raises_on_bad_response():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"error": "Unauthorized"}
    try:
        connector.get_order("111-222-333")
        assert False, "Expected KeyError"
    except KeyError:
        pass


# --- search_returns ---

def test_search_returns_raises_not_implemented():
    connector, _ = make_connector()
    try:
        connector.search_returns(filter_params={})
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        pass


# --- get_listing ---

def test_get_listing_calls_correct_endpoint():
    connector, mock_auth = make_connector()
    connector.get_listing("MY-SKU-123")
    call_kwargs = mock_auth.make_request.call_args
    assert "MY-SKU-123" in call_kwargs[1]["endpoint"]


def test_get_listing_returns_response():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"attributes": {}}
    response = connector.get_listing("MY-SKU-123")
    assert response is not None


# --- create_report (from AmazonReportHandler mixin) ---

def test_create_report_calls_correct_endpoint():
    connector, mock_auth = make_connector()
    connector.create_report(report_type="GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE")
    call_kwargs = mock_auth.make_request.call_args
    assert call_kwargs[0][1] == "reports/2021-06-30/reports"


def test_create_report_returns_response():
    connector, mock_auth = make_connector()
    mock_auth.make_request.return_value.json.return_value = {"reportId": "abc123"}
    response = connector.create_report(report_type="GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE")
    assert response is not None


# --- get_report_info (from AmazonReportHandler mixin) ---

def test_get_report_info_calls_correct_endpoint():
    connector, mock_auth = make_connector()
    connector.get_report_info("abc123")
    call_kwargs = mock_auth.make_request.call_args
    assert "abc123" in call_kwargs[0][1]


# --- get_doc_url (from AmazonReportHandler mixin) ---

def test_get_doc_url_calls_correct_endpoint():
    connector, mock_auth = make_connector()
    connector.get_doc_url("doc456")
    call_kwargs = mock_auth.make_request.call_args
    assert "doc456" in call_kwargs[0][1]
