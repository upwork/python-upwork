import upwork
from upwork.routers.organization import companies
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_list(mocked_method):
    companies.Api(upwork.Client).get_list()
    mocked_method.assert_called_with("/hr/v2/companies")


@patch.object(upwork.Client, "get")
def test_get_specific(mocked_method):
    companies.Api(upwork.Client).get_specific("reference")
    mocked_method.assert_called_with("/hr/v2/companies/reference")


@patch.object(upwork.Client, "get")
def test_get_teams(mocked_method):
    companies.Api(upwork.Client).get_teams("reference")
    mocked_method.assert_called_with("/hr/v2/companies/reference/teams")


@patch.object(upwork.Client, "get")
def test_users(mocked_method):
    companies.Api(upwork.Client).get_users("reference")
    mocked_method.assert_called_with("/hr/v2/companies/reference/users")
