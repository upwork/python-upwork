import upwork
from upwork.routers.organization import teams
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_list(mocked_method):
    """
    Return a list of test test methods.

    Args:
        mocked_method: (todo): write your description
    """
    teams.Api(upwork.Client).get_list()
    mocked_method.assert_called_with("/hr/v2/teams")


@patch.object(upwork.Client, "get")
def test_get_users_in_team(mocked_method):
    """
    Retrieve the team s users.

    Args:
        mocked_method: (todo): write your description
    """
    teams.Api(upwork.Client).get_users_in_team("reference")
    mocked_method.assert_called_with("/hr/v2/teams/reference/users")
