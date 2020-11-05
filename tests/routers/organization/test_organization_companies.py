import upwork
from upwork.routers.organization import companies
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_list(mocked_method):
    """
    Return a list of all the list of a method.

    Args:
        mocked_method: (todo): write your description
    """
    companies.Api(upwork.Client).get_list()
    mocked_method.assert_called_with("/hr/v2/companies")


@patch.object(upwork.Client, "get")
def test_get_specific(mocked_method):
    """
    Retrieve the test method exists.

    Args:
        mocked_method: (todo): write your description
    """
    companies.Api(upwork.Client).get_specific("reference")
    mocked_method.assert_called_with("/hr/v2/companies/reference")


@patch.object(upwork.Client, "get")
def test_get_teams(mocked_method):
    """
    Get all teams.

    Args:
        mocked_method: (todo): write your description
    """
    companies.Api(upwork.Client).get_teams("reference")
    mocked_method.assert_called_with("/hr/v2/companies/reference/teams")


@patch.object(upwork.Client, "get")
def test_users(mocked_method):
    """
    Test for all users.

    Args:
        mocked_method: (todo): write your description
    """
    companies.Api(upwork.Client).get_users("reference")
    mocked_method.assert_called_with("/hr/v2/companies/reference/users")
