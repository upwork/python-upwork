import upwork
from upwork.routers import auth
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_user_info(mocked_method):
    """
    Get user info.

    Args:
        mocked_method: (todo): write your description
    """
    auth.Api(upwork.Client).get_user_info()
    mocked_method.assert_called_with("/auth/v1/info")
