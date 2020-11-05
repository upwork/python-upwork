import upwork
from upwork.routers.organization import users
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_my_info(mocked_method):
    """
    Get test information about the test method.

    Args:
        mocked_method: (todo): write your description
    """
    users.Api(upwork.Client).get_my_info()
    mocked_method.assert_called_with("/hr/v2/users/me")


@patch.object(upwork.Client, "get")
def test_get_specific(mocked_method):
    """
    Get test test method.

    Args:
        mocked_method: (todo): write your description
    """
    users.Api(upwork.Client).get_specific("reference")
    mocked_method.assert_called_with("/hr/v2/users/reference")
