import upwork
from upwork.routers.jobs import search
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_find(mocked_method):
    """
    Find the test methods of the given mocked.

    Args:
        mocked_method: (todo): write your description
    """
    search.Api(upwork.Client).find({"a": "b"})
    mocked_method.assert_called_with("/profiles/v2/search/jobs", {"a": "b"})
