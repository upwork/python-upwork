import upwork
from upwork.routers.hr import roles
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_all(mocked_method):
    """
    Get all available test methods.

    Args:
        mocked_method: (todo): write your description
    """
    roles.Api(upwork.Client).get_all()
    mocked_method.assert_called_with("/hr/v2/userroles")


@patch.object(upwork.Client, "get")
def test_get_by_specific_user(mocked_method):
    """
    Get user by user.

    Args:
        mocked_method: (todo): write your description
    """
    roles.Api(upwork.Client).get_by_specific_user("reference")
    mocked_method.assert_called_with("/hr/v2/userroles/reference")
