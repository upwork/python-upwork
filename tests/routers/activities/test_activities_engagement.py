import upwork
from upwork.routers.activities import engagement
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_specific(mocked_method):
    engagement.Api(upwork.Client).get_specific("1234")
    mocked_method.assert_called_with("/tasks/v2/tasks/contracts/1234")


@patch.object(upwork.Client, "put")
def test_assign(mocked_method):
    engagement.Api(upwork.Client).assign("company", "team", "1234", {"a": "b"})
    mocked_method.assert_called_with(
        "/otask/v1/tasks/companies/company/teams/team/engagements/1234/tasks",
        {"a": "b"},
    )


@patch.object(upwork.Client, "put")
def test_assign_to_engagement(mocked_method):
    engagement.Api(upwork.Client).assign_to_engagement("1234", {"a": "b"})
    mocked_method.assert_called_with("/tasks/v2/tasks/contracts/1234", {"a": "b"})
