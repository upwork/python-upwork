import upwork
from upwork.routers.freelancers import profile
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_specific(mocked_method):
    """
    Retrieve the test for the given method.

    Args:
        mocked_method: (todo): write your description
    """
    profile.Api(upwork.Client).get_specific("key")
    mocked_method.assert_called_with("/profiles/v1/providers/key")


@patch.object(upwork.Client, "get")
def test_get_specific_brief(mocked_method):
    """
    Determine the test bcbio test.

    Args:
        mocked_method: (todo): write your description
    """
    profile.Api(upwork.Client).get_specific_brief("key")
    mocked_method.assert_called_with("/profiles/v1/providers/key/brief")
