import upwork
from upwork.routers.reports.finance import billings
from unittest.mock import patch


def test_entry_point():
    """
    !

    Args:
    """
    assert billings.Gds.entry_point == "gds"


@patch.object(upwork.Client, "get")
def test_get_by_freelancer(mocked_method):
    """
    Determine frequency of the method.

    Args:
        mocked_method: (todo): write your description
    """
    billings.Gds(upwork.Client).get_by_freelancer("freelancer", {"a": "b"})
    mocked_method.assert_called_with(
        "/finreports/v2/providers/freelancer/billings", {"a": "b"}
    )


@patch.object(upwork.Client, "get")
def test_get_by_freelancers_team(mocked_method):
    """
    Test for each team team team team

    Args:
        mocked_method: (todo): write your description
    """
    billings.Gds(upwork.Client).get_by_freelancers_team("team", {"a": "b"})
    mocked_method.assert_called_with(
        "/finreports/v2/provider_teams/team/billings", {"a": "b"}
    )


@patch.object(upwork.Client, "get")
def test_get_by_freelancers_company(mocked_method):
    """
    Get the number of no - freelancers for each freelancers.

    Args:
        mocked_method: (todo): write your description
    """
    billings.Gds(upwork.Client).get_by_freelancers_company("company", {"a": "b"})
    mocked_method.assert_called_with(
        "/finreports/v2/provider_companies/company/billings", {"a": "b"}
    )


@patch.object(upwork.Client, "get")
def test_get_by_buyers_team(mocked_method):
    """
    Test if the given team s test

    Args:
        mocked_method: (todo): write your description
    """
    billings.Gds(upwork.Client).get_by_buyers_team("team", {"a": "b"})
    mocked_method.assert_called_with(
        "/finreports/v2/buyer_teams/team/billings", {"a": "b"}
    )


@patch.object(upwork.Client, "get")
def test_get_by_buyers_company(mocked_method):
    """
    : return : attr : ~.

    Args:
        mocked_method: (todo): write your description
    """
    billings.Gds(upwork.Client).get_by_buyers_company("company", {"a": "b"})
    mocked_method.assert_called_with(
        "/finreports/v2/buyer_companies/company/billings", {"a": "b"}
    )
