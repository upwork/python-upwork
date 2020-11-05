import upwork
from upwork.routers.hr.freelancers import offers
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_list(mocked_method):
    """
    Get test list of a method.

    Args:
        mocked_method: (todo): write your description
    """
    offers.Api(upwork.Client).get_list({})
    mocked_method.assert_called_with("/offers/v1/contractors/offers", {})


@patch.object(upwork.Client, "get")
def test_get_specific(mocked_method):
    """
    Test if the test method.

    Args:
        mocked_method: (todo): write your description
    """
    offers.Api(upwork.Client).get_specific("reference")
    mocked_method.assert_called_with("/offers/v1/contractors/offers/reference")


@patch.object(upwork.Client, "post")
def test_actions(mocked_method):
    """
    Test for all actions.

    Args:
        mocked_method: (todo): write your description
    """
    offers.Api(upwork.Client).actions("reference", {"a": "b"})
    mocked_method.assert_called_with(
        "/offers/v1/contractors/actions/reference", {"a": "b"}
    )
