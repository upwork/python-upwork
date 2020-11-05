import upwork
from upwork.routers.hr import submissions
from unittest.mock import patch


@patch.object(upwork.Client, "post")
def test_request_approval(mocked_method):
    """
    Test if the request is allowed.

    Args:
        mocked_method: (todo): write your description
    """
    submissions.Api(upwork.Client).request_approval({"a": "b"})
    mocked_method.assert_called_with("/hr/v3/fp/submissions", {"a": "b"})


@patch.object(upwork.Client, "put")
def test_approve(mocked_method):
    """
    Approve a test method.

    Args:
        mocked_method: (todo): write your description
    """
    submissions.Api(upwork.Client).approve("submission", {"a": "b"})
    mocked_method.assert_called_with(
        "/hr/v3/fp/submissions/submission/approve", {"a": "b"}
    )


@patch.object(upwork.Client, "put")
def test_reject(mocked_method):
    """
    Rejects all the submissions.

    Args:
        mocked_method: (todo): write your description
    """
    submissions.Api(upwork.Client).reject("submission", {"a": "b"})
    mocked_method.assert_called_with(
        "/hr/v3/fp/submissions/submission/reject", {"a": "b"}
    )
