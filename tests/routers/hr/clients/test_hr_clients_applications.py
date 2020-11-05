import upwork
from upwork.routers.hr.clients import applications
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_list(mocked_method):
    """
    Get list of test methods to test method.

    Args:
        mocked_method: (todo): write your description
    """
    applications.Api(upwork.Client).get_list({"a": "b"})
    mocked_method.assert_called_with("/hr/v4/clients/applications", {"a": "b"})


@patch.object(upwork.Client, "get")
def test_get_specific(mocked_method):
    """
    Test for test test test.

    Args:
        mocked_method: (todo): write your description
    """
    applications.Api(upwork.Client).get_specific("reference", {"a": "b"})
    mocked_method.assert_called_with(
        "/hr/v4/clients/applications/reference", {"a": "b"}
    )
