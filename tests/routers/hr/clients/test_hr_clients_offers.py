import upwork
from upwork.routers.hr.clients import offers
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_list(mocked_method):
    """
    Get list of a list.

    Args:
        mocked_method: (todo): write your description
    """
    offers.Api(upwork.Client).get_list({"a": "b"})
    mocked_method.assert_called_with("/offers/v1/clients/offers", {"a": "b"})


@patch.object(upwork.Client, "get")
def test_get_specific(mocked_method):
    """
    Retrieve test test.

    Args:
        mocked_method: (todo): write your description
    """
    offers.Api(upwork.Client).get_specific("reference", {"a": "b"})
    mocked_method.assert_called_with("/offers/v1/clients/offers/reference", {"a": "b"})


@patch.object(upwork.Client, "post")
def test_make_offer(mocked_method):
    """
    Make a method for the given method.

    Args:
        mocked_method: (todo): write your description
    """
    offers.Api(upwork.Client).make_offer({"a": "b"})
    mocked_method.assert_called_with("/offers/v1/clients/offers", {"a": "b"})
