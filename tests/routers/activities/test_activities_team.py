import upwork
from upwork.routers.activities import team
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_list(mocked_method):
    """
    Get the list of all of a team.

    Args:
        mocked_method: (todo): write your description
    """
    team.Api(upwork.Client).get_list("company", "team")
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/teams/team/tasks"
    )


@patch.object(upwork.Client, "get")
def test_get_specific_list(mocked_method):
    """
    Get the list of test methods.

    Args:
        mocked_method: (todo): write your description
    """
    team.Api(upwork.Client).get_specific_list("company", "team", "code")
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/teams/team/tasks/code"
    )


@patch.object(upwork.Client, "post")
def test_add_activity(mocked_method):
    """
    Add the activity to the activity to the activity.

    Args:
        mocked_method: (todo): write your description
    """
    team.Api(upwork.Client).add_activity("company", "team", {"a": "b"})
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/teams/team/tasks", {"a": "b"}
    )


@patch.object(upwork.Client, "put")
def test_update_activities(mocked_method):
    """
    Update the activities.

    Args:
        mocked_method: (todo): write your description
    """
    team.Api(upwork.Client).update_activities("company", "team", "code", {"a": "b"})
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/teams/team/tasks/code", {"a": "b"}
    )


@patch.object(upwork.Client, "put")
def test_archive_activities(mocked_method):
    """
    Test for an archive archive archive exists.

    Args:
        mocked_method: (todo): write your description
    """
    team.Api(upwork.Client).archive_activities("company", "team", "code")
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/teams/team/archive/code"
    )


@patch.object(upwork.Client, "put")
def test_unarchive_activities(mocked_method):
    """
    Decide whether the unarchive are unarchive.

    Args:
        mocked_method: (todo): write your description
    """
    team.Api(upwork.Client).unarchive_activities("company", "team", "code")
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/teams/team/unarchive/code"
    )


@patch.object(upwork.Client, "put")
def test_update_batch(mocked_method):
    """
    Updates the batch of a batch.

    Args:
        mocked_method: (todo): write your description
    """
    team.Api(upwork.Client).update_batch("company", {"a": "b"})
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/tasks/batch", {"a": "b"}
    )
