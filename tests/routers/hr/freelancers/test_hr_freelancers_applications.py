import upwork
from upwork.routers.hr.freelancers import applications
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_list(mocked_method):
    """
    Get list of test methods.

    Args:
        mocked_method: (todo): write your description
    """
    applications.Api(upwork.Client).get_list({})
    mocked_method.assert_called_with("/hr/v4/contractors/applications", {})


@patch.object(upwork.Client, "get")
def test_get_specific(mocked_method):
    """
    Determine the method.

    Args:
        mocked_method: (todo): write your description
    """
    applications.Api(upwork.Client).get_specific("reference")
    mocked_method.assert_called_with("/hr/v4/contractors/applications/reference")
