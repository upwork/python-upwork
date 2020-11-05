import upwork
from upwork.routers.jobs import profile
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_specific(mocked_method):
    """
    Retrieve the test for the given method.

    Args:
        mocked_method: (todo): write your description
    """
    profile.Api(upwork.Client).get_specific("key")
    mocked_method.assert_called_with("/profiles/v1/jobs/key")
