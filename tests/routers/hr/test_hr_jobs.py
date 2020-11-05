import upwork
from upwork.routers.hr import jobs
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_list(mocked_method):
    """
    Get a list of a test.

    Args:
        mocked_method: (todo): write your description
    """
    jobs.Api(upwork.Client).get_list({"a": "b"})
    mocked_method.assert_called_with("/hr/v2/jobs", {"a": "b"})


@patch.object(upwork.Client, "get")
def test_get_specific(mocked_method):
    """
    Deter test jobs that case.

    Args:
        mocked_method: (todo): write your description
    """
    jobs.Api(upwork.Client).get_specific("key")
    mocked_method.assert_called_with("/hr/v2/jobs/key")


@patch.object(upwork.Client, "post")
def test_post_job(mocked_method):
    """
    Test for jobs in - memory.

    Args:
        mocked_method: (todo): write your description
    """
    jobs.Api(upwork.Client).post_job({"a": "b"})
    mocked_method.assert_called_with("/hr/v2/jobs", {"a": "b"})


@patch.object(upwork.Client, "put")
def test_edit_job(mocked_method):
    """
    Test for the test job.

    Args:
        mocked_method: (todo): write your description
    """
    jobs.Api(upwork.Client).edit_job("key", {"a": "b"})
    mocked_method.assert_called_with("/hr/v2/jobs/key", {"a": "b"})


@patch.object(upwork.Client, "delete")
def test_delete_job(mocked_method):
    """
    Delete jobs from a test job.

    Args:
        mocked_method: (todo): write your description
    """
    jobs.Api(upwork.Client).delete_job("key", {"a": "b"})
    mocked_method.assert_called_with("/hr/v2/jobs/key", {"a": "b"})
