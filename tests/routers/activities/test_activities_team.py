import upwork
from upwork.routers.activities import team
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_list(mocked_method):
    team.Api(upwork.Client).get_list("company", "team")
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/teams/team/tasks"
    )


@patch.object(upwork.Client, "get")
def test_get_specific_list(mocked_method):
    team.Api(upwork.Client).get_specific_list("company", "team", "code")
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/teams/team/tasks/code"
    )


@patch.object(upwork.Client, "post")
def test_add_activity(mocked_method):
    team.Api(upwork.Client).add_activity("company", "team", {"a": "b"})
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/teams/team/tasks", {"a": "b"}
    )


@patch.object(upwork.Client, "put")
def test_update_activities(mocked_method):
    team.Api(upwork.Client).update_activities("company", "team", "code", {"a": "b"})
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/teams/team/tasks/code", {"a": "b"}
    )


@patch.object(upwork.Client, "put")
def test_archive_activities(mocked_method):
    team.Api(upwork.Client).archive_activities("company", "team", "code")
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/teams/team/archive/code"
    )


@patch.object(upwork.Client, "put")
def test_unarchive_activities(mocked_method):
    team.Api(upwork.Client).unarchive_activities("company", "team", "code")
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/teams/team/unarchive/code"
    )


@patch.object(upwork.Client, "put")
def test_update_batch(mocked_method):
    team.Api(upwork.Client).update_batch("company", {"a": "b"})
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/tasks/batch", {"a": "b"}
    )
